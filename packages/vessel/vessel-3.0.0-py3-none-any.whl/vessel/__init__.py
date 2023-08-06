
from . import _builds
from . import _updates


__all__ = ('Field', 'missing', 'ObjectBase', 'object', 'ListBase', 'list',
           'DictBase', 'dict', 'update')


class Field(_builds.Field):

    """
    Field(type=None, make=None, name=None)

    Describes how an :func:`.object` instance key should be handled.

    :param func type:
        Called with ``(data)`` for creation of new value.
    :param func make:
        Called with ``self`` upon attribute access. Close to :class:`property`.
    :param str name:
        Exclusive alternative to accessing an data value.
    """

    __slots__ = ()


missing = _builds.missing
"""
Returned upon accessing valid but empty attribute. Exhibits negative booleanity.
"""


class ObjectBase:

    """
    Default ABC for :func:`.object` classes.
    """

    __slots__ = ()


def object(*args, cls = ObjectBase, **kwargs):

    """
    object(info, identify=None, cls=ObjectBase, **behave)

    Create a class supporting dynamically updated data.

    :param dict[str,Field] info:
        Determines how to handle incoming data.
    :param func identify:
        Should return a hash for caching.
    :param type cls:
        Base class for created class.

    .. code-block:: py

        User_info = {
            'id': vessel.Field(
                type = int
            ),
            'username': vessel.Field(
                type = str,
                name = 'name'
            ),
            'tag': vessel.Field(
                type = str
            ),
            'display': vessel.Field(
                make = lambda self: f'{self.name}#{self.tag}'
            )
        }

        User_identify = lambda data: int(data['id'])

        User = vessel.object(User_info, User_identify)

        user = User(
            {
                'id': 0,
                'username': 'Exa',
                'tag': '0000'
            }
        )

        print(user.display)

    Above snippet prints ``Exa#0000``.

    .. note::

        When calling generated classes, the **same** instance will be returned
        for datas whose identity matches an existing one. To disable this
        behavior temporarily, use ``unique = True``. This is incosequential for
        classes generated without ``identify``.

        .. code-block:: py

            data = {'id': 0, ...}
            user0 = User(data)
            user1 = User(data)
            user2 = User(data, unique = True)
            print(user0 is user1)
            print(user0 is user2)

        Above snipper prints ``True`` and ``False``
    """

    return _builds.build_vessel(*args, cls = cls, **kwargs)


class ListBase:

    """
    Default ABC for :func:`.list` classes.
    """

    __slots__ = ()


def list(*args, cls = ListBase, **kwargs):

    """
    list(type, compare, cls=ListBase, **behave)

    Create a class supporting :class:`list` access operations hosting objects.

    :param func type:
        Called with ``(data)`` for creation of new value.
    :param func compare:
        Called with ``(root, data)`` and should return :class:`bool` for
        whether their identities match.
    :param type cls:
        Base class for created class.

    .. code-block::

        User_compare = lambda self, data: self.id == User_identify(data)

        Account_info = {
            'owner': vessel.Field(
                type = User
            ),
            'friends': vessel.Field(
                type = vessel.list(User, User_compare)
            )
        }

        Account = vessel.object(Account_info)

        account = Account(
            {
                'owner': {
                    'id': 0,
                    'username': 'Exa',
                    'tag': '0000',
                },
                'friends': [
                    {
                        'id': 1,
                        'username': 'Rob',
                        'tag': '1234'
                    },
                    {
                        'id': 2,
                        'username': 'Nil',
                        'tag': '5678'
                    }
                ]
            }
        )

        for friend in account.friends:
            print(friend.display)

    Above snippet will print ``Rob#1234`` and ``Nil#5678``.
    """

    return _builds.build_list(*args, cls = ListBase, **kwargs)


class DictBase:

    """
    Default ABC for :func:`.dict` classes.
    """

    __slots__ = ()


def dict(*args, cls = DictBase, **kwargs):

    """
    dict(type, identify, cls=DictBase, **behave)

    Create a class supporting :class:`dict` access operations hosting objects.

    :param func type:
        Called with ``(data)`` for creation of new value.
    :param func compare:
        Called with ``(data)`` and should return respective key.
    :param type cls:
        Base class for created class.

    .. code-block:: py

        Account_info = {
            'owner': vessel.Field(
                type = User
            ),
            'friends': vessel.Field(
                type = vessel.dict(User, User_identify, flush = True)
            )
        }

        account = Account({...})

        for friend in account.friends:
            print(friend.display)

        print(account.friends[1].name)

    Above snippet will print ``Rob#1234``, ``Nil#5678`` and ``Rob``.

    .. note::

        Unlike normal :class:`dict`\s, direct iteration yields values instead of
        keys.
    """

    return _builds.build_dict(*args, cls = DictBase, **kwargs)


def update(*args, **kwargs):

    """
    update(root, data, flush=?)

    Updates an :func:`.object`, :func:`.list` or :func:`.dict` result with new
    data.

    - Mutates data when identity matches with new data.
    - Removes old data when identity does not match with new data if ``flush``.
    - Appends new data when identity does not match with old data.

    :param object root:
        Initial value.
    :param dict or list data:
        Stuff to update root with.
    :param bool flush:
        Whether to remove redundant entries.

    ``flush`` is ``False`` by default except for :func:`.list` results.

    ``data`` **must** be :class:`dict` for :func:`.object` results, and
    :class:`list` otherwise.

    .. note::

        ``**behave`` in other functions overwrites defaults for optional
        arguments.

    .. code-block:: py

        vessel.update(
            account,
            {
                'owner': {
                    'tag': '9012'
                },
                'friends': [
                    {
                        'id': 1,
                        'username': 'Robbert'
                    },
                    {
                        'id': 3,
                        'username': 'Cul',
                        'tag': '3456'
                    }
                ]
            }
        )

        for friend in account.friends:
            print(friend.display)

    Above snippet will print ``Robbert#1234`` and ``Cull#3456``.

    ``Nil`` was removed because ``flush=True`` when using :func:`.dict` for
    ``'friends'``.

    .. note::

      Generated class instances are not designed for mutation outside of
      :func:`.update`.
    """

    return _updates.any_(*args, **kwargs)
