'''SerialAlchemy
Dead simple object serialization for SQLAlchemy

'''

from sqlalchemy import inspect, DateTime, Date, Time, processors, event
from decimal import Decimal
from datetime import datetime, date, timedelta, time
from sqlalchemy.ext.hybrid import hybrid_property

import inspect as inspectPy

import re
from collections import abc
import json


class SerialAlchemyError(Exception):
    pass

__all__ = [
        'serializable_property',
        'Serializable',
        ]

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def convert_class(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


primitives = (int, str, bytes, float, dict, list, type(None),)


def _get_value(obj, field):
    global primitives

    value = getattr(obj, field)

    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, datetime) or isinstance(value, date) or\
            isinstance(value, time):
        return str(value)
    elif isinstance(value, timedelta):
        return float(value.total_seconds())
    elif isinstance(value, (set, frozenset,)):
        return list(value)
    elif not isinstance(value, primitives):
        return str(value)

    return value


def _get_serializable_properties(obj, attrs, loaded):
    all_members = set([f for f in dir(obj) if not f.startswith('_')])
    properties = all_members - set(attrs) - set(loaded)


    if not hasattr(obj, '__class__'):
        return []

    cls = obj.__class__
    propout = []

    for prop in properties:
        if isinstance(getattr(cls, prop), serializable_property):
            if hasattr(obj, prop):
                propout.append(prop)
        else:
            attr = getattr(cls, prop)
            should_add = False

            try:
                should_add = isinstance(attr.descriptor, hybrid_property)
            except AttributeError:
                should_add = False

            if should_add and hasattr(obj, prop):
                propout.append(prop)

    return propout



class serializable_property(property):
    '''Simple wrapper for built-in `property` for explicit serialization of
    class/instance properties.

    As of version 0.2.0, SerialAlchemy will not include a property unless
    it is decorated with `serializable_property` or is a SQLAlchemy
    hybrid_attribute.
    '''
    pass


class Serializable:
    '''Provides serialization and deserialization for data-mapped classes.

    This is a mixin class that provides serializaiton to python dicts and
    object population (deserialization). A method for creating a streaming
    json generator from a result set is also defined.

    The mixin defines two special attributes during SQLAlchemy's
    `mapper_configured` event which are used for json generation.

    :attribute __single__: The name of a single object. If not specified,
        the mapper class name is used, converting camel-case to
        underscore.

    :attribute __plural__: The name of multiple objects. If not specified,
        the mapper's `__tablename__` is used.

    This is my own personal preference, although I'm told a few other people do
    it this way too::
        class User(Base, Serializable):
            __tablename__ = 'users'

            #rest of class definition

    In this example, __single__ = 'user', __plural__ = 'users'.

    Properties must be serialized with the `@serializable_property`
    or the `@hybrid_property` decorator to be included in the output. Functions
    decorated with Python's `property` built-in are ignored.::
        class User(Base, Serializable):
            __tablename__ = 'users'

            #Columns...

            @property
            def one(self):
                """this will not be in the output"""
                return 1

            @serializable_property
            def two(self):
                """this will be in the output"""
                return 2


    Additionally, specific columns can be excluded using the column's info
    attribute::
        class User(Base, Serializable):
            __tablename__ = 'users'

            username = Column(Unicode(100))
            password = Column(UnicodeText,
                info={'serializable': False})

    In this example, password will never be included in the output of
    `to_dict()`.
    '''

    @classmethod
    def _define_special_fields(cls):
        if not hasattr(cls, '__single__') or cls.__single__ is None:
            cls.__single__ = convert_class(cls.__name__)

        if not hasattr(cls, '__plural__') or cls.__plural__ is None:
            if hasattr(cls, '__tablename__'):
                cls.__plural__ = cls.__tablename__
            else:
                cls.__plural__ = cls.__single__


    def to_dict(self, fields=None, relationships=True, mtm_pkonly=True):
        '''Serialize a SQLAlchemy mapper in to a python dictionary.

        :param fields=None: An iterable of field names (str) or None.
            The dictionary returned will include only the fields specified.
            Alternatively, prefixing a field name with a tilde (~) will
            exclude that field from the returned dict. Mixing included and
            excluded field names will ignore the excluded fields.

            Relationship properties can be in this parameter, although will be
            ignored unless the `relationships` parameter is True. Properties of
            related objects are filtered via SQLAlchemy's `load_only` query
            option.

        :param relationships=True: Include or omit relationship properties.
            Output is based on the relationship definition. It will be either
            a list of dicts, or a dict itself based on the `uselist` parameter
            of the relationship function.

            The `fields` paramter does not affect the related object output.
            To filter related object fields, use SQLAlchemy's `load_only`
            device during query construction.

            The related class must also have the `Serializable` mixin.

            *Note: Relationships of related objects are ignored. I couldn't
            see the benefit vs the complexity it would bring.*

        :param mtm_pkonly=True: If True, return only the primary-key for
            secondary objects of a many-to-many relationship. If False,
            all fields of the secondary object will be included, subject
            to the `load_only` filter.
        '''

        output = {}

        includes = frozenset()
        excludes = frozenset()

        if fields is not None:
            includes = frozenset([f for f in fields if not f.startswith('~')])
            excludes = frozenset([f[1:] for f in fields if f.startswith('~')])

        info = inspect(self)

        for col in info.mapper.columns:
            field = col.name
            if includes and field not in includes:
                continue
            elif excludes and field in excludes:
                continue
            elif hasattr(col, 'info'):
                if 'serializable' in col.info and not col.info['serializable']:
                    continue

            output[field] = _get_value(self, field)


        if relationships:
            for field, relation in info.mapper.relationships.items():
                if includes and field not in includes:
                    continue
                elif excludes and field in excludes:
                    continue

                data = getattr(self, field)
                relout = None

                if relation.uselist:
                    relout = []
                    for obj in data:
                        if isinstance(obj, Serializable):
                            if relation.secondary is not None and mtm_pkonly:
                                relinfo = inspect(obj.__class__)
                                pkeys = relinfo.primary_key
                                out = []
                                for pk in pkeys:
                                    val = getattr(obj, pk.name)
                                    out.append(val)
                                relout.extend(out)
                            else:
                                relinfo = inspect(obj)
                                relfields = [k for k in relinfo.dict.keys() if
                                        not k.startswith('_')]

                                props = _get_serializable_properties(obj,
                                        relinfo.attrs.keys(),
                                        relfields)

                                relfields.extend(props)

                                relout.append(obj.to_dict(relfields,
                                    relationships=False,
                                    mtm_pkonly=mtm_pkonly))

                else:
                    if data and isinstance(data, Serializable):
                        relinfo = inspect(data)
                        relfields = [k for k in relinfo.dict.keys() if not
                                k.startswith('_')]

                        props = _get_serializable_properties(data,
                                relinfo.attrs.keys(), relfields)

                        relfields.extend(props)

                        relout = data.to_dict(relfields,
                                relationships=False,
                                mtm_pkonly=mtm_pkonly)

                if relout:
                    output[field] = relout


        properties = _get_serializable_properties(self, info.attrs.keys(), [])

        for prop in properties:
            if includes and prop not in includes:
                continue
            elif excludes and prop in excludes:
                continue

            if hasattr(self, prop):
                output[prop] = _get_value(self, prop)

        return output

    def populate(self, data, skip_fields=None, swallow_exceptions=False):
        '''Populate object from a dict of fields.

        *This method does not populate relationships*. It is recommended
        to override the method and handle them manually.

        Values for relationship attributes can be supplied in the `data`
        parameter and will be safely ignored.

        :param data: A dict whose keys match the object attributes.
        :param skip_fields: An iterable of attributes to not set, whether they
            are in the data parameter or not.
        :param swallow_exceptions: Boolean flag to blanket handle all
            exceptions when setting values, and return a list of Error objects.
            Hint: use with SQLAlchemy's `validates` decorator.
            Default: False
        '''

        if skip_fields is None:
            skip_fields = []

        info = inspect(self)
        mapper = info.mapper
        errors = []

        for col in mapper.columns:
            if col.name in skip_fields:
                continue
            elif col.name in data:
                if isinstance(col.type, DateTime):
                    value = processors.str_to_datetime(data[col.name])
                elif isinstance(col.type, Date):
                    value = processors.str_to_date(data[col.name])
                elif isinstance(col.type, Time):
                    value = processors.str_to_time(data[col.name])
                else:
                    value = data[col.name]

                try:
                    setattr(self, col.name, value)
                except Exception as ex:
                    if not swallow_exceptions:
                        raise ex
                    errors.append(ex)

        return errors


    @classmethod
    def json_factory(cls, resultset, fields=None, relationships=True,
            mtm_pkonly=True):
        '''Create a generator to serialize a result or result set to JSON.

        This classmethod creates a generator that streams JSON data, wrapping
        the set in the pluralized name if the object is iterable (i.e. a list),
        or in the singular name if not.

        :param resultset: An iterable (e.g. list or SQLAlchemy query), or a
            single mapped instance.

        :param fields=None: Passed directly to `to_dict`
        :param relationships=True: Passed directly to `to_dict`
        :param mtm_pkonly=True: Passed directly to `to_dict`

        '''

        def generator():
            if isinstance(resultset, abc.Iterable):
                yield '{"%s": [' % cls.__plural__

                iresult = iter(resultset)
                try:
                    prev = next(iresult)

                    for row in iresult:
                        yield json.dumps(prev.to_dict(fields, relationships,
                            mtm_pkonly)) + ','
                        prev = row

                    yield json.dumps(prev.to_dict(fields, relationships, mtm_pkonly))
                except StopIteration:
                    pass
                except Exception as ex:
                    raise ex
                finally:
                    yield ']}'

            elif resultset is not None:
                yield json.dumps({cls.__single__: resultset.to_dict(fields,
                    relationships, mtm_pkonly)})
            else:
                yield json.dumps({cls.__single__: None})

        return generator

    @classmethod
    def to_json(cls, resultset, fields=None, relationships=True,
            mtm_pkonly=True):
        '''Dump a result or result set to JSON.

        This classmethod is similar to `json_factory` but does not create a
        generator for streaming output. The results are wrapped in the
        pluralized name if the object is iterable (i.e. a list), or in the
        singular name if not.

        :param resultset: An iterable (e.g. list or SQLAlchemy query), or a
            single mapped instance.

        :param fields=None: Passed directly to `to_dict`
        :param relationships=True: Passed directly to `to_dict`
        :param mtm_pkonly=True: Passed directly to `to_dict`

        '''

        if isinstance(resultset, abc.Iterable):
            seritems = []

            for item in resultset:
                seritems.append(item.to_dict(fields, relationships,
                    mtm_pkonly))

            return json.dumps({cls.__plural__: seritems})
        elif resultset is not None:
            return json.dumps({cls.__single__: resultset.to_dict(fields,
                relationships, mtm_pkonly)})
        else:
            return json.dumps({cls.__single__: None})

    @classmethod
    def schema_info(cls):
        '''Return schema metadata as a dict.

        This classmethod returns information about the table columns.

        *Note*: this function is experimental and may not stay in the library
        '''
        info = inspect(cls)

        metainfo = {}

        for name, col in info.c.items():
            if 'serializable' in col.info and not col.info['serializable']:
                continue

            try:
                pytype = col.type.python_type.__qualname__
            except NotImplementedError:
                pytype = 'bytes'

            m = {
                "type": pytype,
                "auto": col.autoincrement,
                "pk": col.primary_key,
                "default": col.default,
                "nullable": col.nullable,
            }

            if hasattr(col.type, 'length'):
                m['length'] = col.type.length
            if hasattr(col.type, 'precision'):
                m['precision'] = col.type.precision
                m['scale'] = col.type.scale
            if hasattr(col.type, 'enums'):
                m['enums'] = col.type.enums

            metainfo[name] = m

        for name, rel in info.relationships.items():
            if 'serializable' in col.info and not col.info['serializable']:
                continue

            m = {
                "type": "relationship",
                "target": rel.target.name,
                "many": rel.uselist,
                "manytomany": rel.secondary is not None,
            }

            metainfo[name] = m

        return metainfo

    @classmethod
    async def async_factory(cls, resultset, fields=None, relationships=True,
            mtm_pkonly=True, encoding='utf-8'):
        '''Create an async generator to serialize a result or result set to JSON.

        This classmethod creates a generator that streams JSON data, wrapping
        the set in the pluralized name if the object is iterable (i.e. a list),
        or in the singular name if not.

        :param resultset: An iterable (e.g. list or SQLAlchemy query), or a
            single mapped instance.

        :param fields=None: Passed directly to `to_dict`
        :param relationships=True: Passed directly to `to_dict`
        :param mtm_pkonly=True: Passed directly to `to_dict`
        :param encoding='utf-8': Encoding for the result. Defaults to 'utf-8'.
            Set to `False` to return an unencoded str.
            (This is mostly because Hypercorn doesn't seem to encode a
            response stream the way Werkzeug does).
        '''

        async def generator():
            if isinstance(resultset, abc.Iterable):
                start = '{"%s": [' % cls.__plural__
                if encoding:
                    start = start.encode(encoding)

                yield start

                iresult = iter(resultset)
                try:
                    prev = next(iresult)

                    for row in iresult:
                        r = json.dumps(prev.to_dict(fields, relationships,
                            mtm_pkonly)) + ','

                        if encoding:
                            r = r.encode(encoding)

                        yield r

                        prev = row

                    p = json.dumps(prev.to_dict(fields, relationships, mtm_pkonly))
                    if encoding:
                        p = p.encode(encoding)

                    yield p
                except StopIteration:
                    pass
                except Exception as ex:
                    raise ex
                finally:
                    end = ']}'
                    if encoding:
                        end = end.encode(encoding)

                    yield end

            elif resultset is not None:
                s = json.dumps({cls.__single__: resultset.to_dict(fields,
                    relationships, mtm_pkonly)})

                if encoding:
                    s = s.encode(encoding)

                yield s
            else:
                empty = json.dumps({cls.__single__: None})
                if encoding:
                    empty = empty.encode(encoding)

                yield empty

        return generator


@event.listens_for(Serializable, 'mapper_configured', propagate=True)
def add_special_fields(mapper, cls):
    cls._define_special_fields()

