
from . import _share


__all__ = ()


def unit(info, root, data, flush = False):

    left = set(root if flush else ())

    for (name, subdata) in data.items():

        try:
            field = info[name]
        except KeyError:
            continue

        left.discard(name)

        try:
            value = root[name]
        except KeyError:
            value = root[name] = field.type(subdata)
            continue

        try:
            any_(value, subdata)
        except ValueError:
            root[name] = subdata

    for name in left:
        try:
            del data[name]
        except KeyError:
            continue


def list_(compare, build, root, data, flush = True):

    rindex = 0

    while True:
        try:
            value = root[rindex]
        except IndexError:
            break
        for (dindex, subdata) in enumerate(data):
            if not compare(value, subdata):
                continue
            break
        else:
            if flush:
                del root[index]
            continue
        any_(value, subdata)
        del data[dindex]
        rindex += 1

    root.extend(map(build, data))


def dict_(identify, build, root, data, flush = False):

    if identify is None:
        identities = list(data)
        data = data.values()
    else:
        identities = list(map(identify, data))

    for (key, value) in tuple(root.items()):
        for (index, subdata) in enumerate(data):
            identity = identities[index]
            if not key == identity:
                continue
            break
        else:
            if flush:
                del root[key]
            continue
        any_(value, subdata)
        del data[index], identities[index]

    root.update(zip(identities, map(build, data)))


def any_(value, data, **kwargs):

    context = _share.get(value.__class__)

    root = context.datas[value]

    context.update(root, data, **kwargs)
