from random import choice
from . import Str

def __throw(exception):
    raise BaseException(exception)


def get(arr: list or dict = None, key_path: str = '') -> list or None:
    keys = key_path.split('.')

    def dictGet(arr):
        for k in filter(None, keys):
            if k in arr:
                arr = arr[k]
            else:
                return None
        return arr

    def listGet(arr):
        arrs = []
        for item in arr:
            if type(item) == dict:
                add = dictGet(item)
                arrs.append(add)
        return arrs

    if type(arr) == dict:
        return dictGet(arr)
    elif type(arr) == list:
        return listGet(arr)


def column(arr: list = [], key: any = None) -> list or None:
    _raise = 'no {key} in list'.format(key=key)

    if '.' in key:
        return get(arr, key)

    firstType = type(first(arr))

    if firstType in [tuple, list]:
        return list(map(lambda x: x[key] if len(x) - 1 >= key else __throw(_raise), arr))
    elif firstType in [dict]:
        return list(map(lambda x: x[key] if key in x else __throw(_raise), arr))
    else:
        return None


def first(arr: list = []):
    return arr[0]


def last(arr: list = []):
    return arr[-1]


def combine(keys: list = [], values: list = []) -> dict:
    if len(keys) != len(values):
        raise BaseException('keys and values are not equal in number')

    return {x: values[k] for k, x in enumerate(keys)}


def divide(arr: dict = {}) -> tuple:
    return list(arr.keys()), list(arr.values())


def has(arr: dict = {}, key_path: str = '') -> bool:
    check = get(arr=arr, key_path=key_path)

    if type(check) == list:
        check = array_filter(check)
        if len(check) == 0:
            return False

    if check is not None:
        return True
    else:
        return False


def only(arr: dict = {}, keys: list = []) -> dict:
    return {x: arr[x] if x in list(arr.keys()) else __throw('no {key} in list'.format(key=x)) for x in keys}


def pluck(arr: list = [], keys: str = None, vals: str = None) -> dict or list:
    def one():
        allKeys = column(arr=arr, key=keys)
        allValues = column(arr=arr, key=vals)
        return combine(allKeys, allValues)

    def multiple(arr, keys, vals):
        keys = get(arr, keys)
        vals = get(arr, vals)
        return combine(keys, vals)

    if keys is not None and vals is not None:
        if '.' not in keys and '.' not in vals:
            return one()

        elif '.' in keys and '.' in vals:
            return multiple(arr, keys, vals)

    elif keys is not None and vals is None:
        if '.' not in keys:
            return column(arr, keys)

        else:
            keysGet = get(arr, keys)
            valAll = [None for i in range(0, len(keysGet))]
            return combine(keysGet, valAll)

    elif keys is None and vals is not None:
        if '.' not in vals:
            return column(arr, vals)

        else:
            return get(arr, vals)


def prepend(arr: list or dict = [], val: any = None) -> list or dict:
    arr.insert(0, val)
    return arr


def exists(arr: dict or list = None, search: any = None, key: str = None) -> bool:
    srch = arr
    if key is not None:
        srch = get(arr, key)
    elif type(arr) == dict:
        srch = arr.values()

    if search in srch:
        return True
    else:
        return False


def keyExists(arr: dict = {}, val: any = None) -> bool:
    if '.' in val and get(arr, val) is not None:
        return True
    elif val in list(arr.keys()):
        return True
    else:
        return False


def random(arr: list = None):
    return choice(arr)


def wrap(key: str or None = None, val: any = None) -> list or dict:
    if key is None:
        return list()

    elif '.' in key:
        arr = key.split('.')
        news = None
        for s, it in enumerate(reversed(arr)):
            if s == 0:
                news = {it: val}
            else:
                news = dict({it: news})

        return news

    else:
        return [key]


def array_filter(arr: list = []) -> list:
    return list(filter(lambda x: x is not None and x != '', arr))

