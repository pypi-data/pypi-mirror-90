import collections


__all__ = ()


Context = collections.namedtuple(
    'Context',
    'type update datas'
)


contexts = []


def get(type):

    for context in contexts:
        if not issubclass(type, context.type):
            continue
        break
    else:
        raise ValueError('not found')

    return context
