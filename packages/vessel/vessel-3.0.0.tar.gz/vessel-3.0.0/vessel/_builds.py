import collections
import weakref
import itertools

from . import _share
from . import _updates


__all__ = ('Field', 'missing', 'update', 'build_vessel', 'build_list',
           'build_dict')


def _build(create, update, identify, cls):

    datas = weakref.WeakKeyDictionary()

    if identify:
        units = weakref.WeakValueDictionary()
    else:
        units = None

    class Unit(cls):

        __slots__ = ('__weakref__',)

        def __new__(cls, data, *args, unique = False, **kwargs):

            if identify and not unique:
                identity = identify(data)
                try:
                    self = units[identity]
                except KeyError:
                    forge = attach = True
                else:
                    forge = attach = False
            else:
                forge = True
                attach = False

            if forge:
                self = super().__new__(cls)
                if create:
                    datas[self] = create(data)

            if attach:
                units[identity] = self

            if update:
                _updates.any_(self, data)

            return self

    return Unit, datas


def build(create, update, identify, cls = object):

    Unit, datas = _build(create, update, identify, cls)

    context = _share.Context(Unit, update, datas)
    _share.contexts.append(context)

    return Unit


def _get_data(unit):

    context = _share.get(unit.__class__)

    data = context.datas[unit]

    return data


Field = collections.namedtuple(
    'Field',
    'type name make',
    defaults = (None, None, None)
)


missing = type(
    'missing',
    (),
    {
        '__slots__': (),
        '__bool__': False.__bool__,
        '__repr__': lambda self: ''
    }
)()


def build_vessel(info, identify = None, cls = object, **behave):

    def create(data):

        root = {}

        return root

    def update(root, data, **kwargs):

        kwargs = {**behave, **kwargs}

        _updates.unit(info, root, data, **kwargs)

    names = {field.name: name for (name, field) in info.items() if field.name}

    alias = lambda name: names.get(name, name)

    class Vessel(cls):

        __slots__ = ()

        def __getattr__(self, name):

            name = alias(name)

            try:
                field = info[name]
            except KeyError as error:
                raise AttributeError(*error.args) from None

            context = _share.get(self.__class__)

            if field.make:
                return field.make(self)

            data = context.datas[self]

            value = data.get(name, missing)

            return value

        def __repr__(self):

            data = _get_data(self)

            names = map(alias, data.keys())
            values = data.values()
            items = zip(names, values)

            pairs = ', '.join(map('{0[0]}={0[1]}'.format, items))

            return '{0}({1})'.format(self.__class__.__name__, pairs)

    Unit = build(create, update, identify, Vessel)

    return Unit


def _method_data_proxy_wrap(name):

    def function(self, *args, **kwargs):

        data = _get_data(self)

        return getattr(data, name)(*args, **kwargs)

    return function


_collection_names = ('__iter__', '__len__', '__getitem__')


def _collection__repr__(self):

    data = _get_data(self)

    return '{0}({1})'.format(self.__class__.__name__, len(data))


def _collect(cls, names):

    space = {'__slots__': (), '__repr__': _collection__repr__}

    for name in itertools.chain(_collection_names, names):
        space[name] = _method_data_proxy_wrap(name)

    CollectionBase = type('CollectionBase', (cls,), space)

    return CollectionBase


def build_list(make, compare, cls = object, **behave):

    def create(data):

        root = []

        return root

    def update(root, data, **kwargs):

        kwargs = {**behave, **kwargs}

        _updates.list_(compare, make, root, data, **kwargs)

    CollectionBase = _collect(cls, ())

    Unit = build(create, update, None, CollectionBase)

    class List(Unit):

        __slots__ = ()

    return Unit


def build_dict(make, identify, cls = object, **behave):

    def create(data):

        root = {}

        return root

    def update(root, data, **kwargs):

        kwargs = {**behave, **kwargs}

        _updates.dict_(identify, make, root, data, **kwargs)

    CollectionBase = _collect(cls, ('get', 'keys', 'values', 'items'))

    Unit = build(create, update, None, CollectionBase)

    class Dict(Unit):

        __slots__ = ()

        def __iter__(self):

            yield from self.values()

    return Dict
