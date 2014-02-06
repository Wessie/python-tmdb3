import requests


class TMDBError(Exception):
    pass


class API(object):
    registar = {}

    def __init__(self, api_key):
        super(API, self).__init__()

        self.key = api_key

    @classmethod
    def register(cls, name, schema_cls):
        cls.registar[name] = schema_cls

    def _call(self, name):
        schema = self.registar.get(name)

        if not schema:
            raise KeyError("Unsupported API method '%s'" % name)

        # TODO: Make this only be created once
        return create_api_method(self, name, schema)

    def __getattr__(self, key):
        return self._call(key)


class AttributeDict(dict):
    """
    Simple dictionary subclass that supports attribute
    access to the dictionary alongside normal access.
    """
    def __init__(self, dct):
        self.recursive_instantion(dct)

        super(AttributeDict, self).__init__(dct)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return super(State, self).__getattr__(key)

    def __setattr__(self, key, value):
        super(AttributeDict, self).__setattr__(key, value)

    def __delattr__(self, key):
        del self[key]

    def recursive_instantion(self, dct):
        """
        Recursively check if there are any other dicts
        nested in our `self`. Make all we find also an
        `AttributeDict`.

        note: This only checks recursively in dicts and lists
        """
        for key, value in dct.items():
            if isinstance(value, dict):
                dct[key] = AttributeDict(value)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        value[i] = AttributeDict(item)


def create_api_method(api, name, cls):
    def call(**params):
        url = cls.url.format(**params)

        params['api_key'] = api.key

        try:
            result = requests.get(url, params=params)
            result.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise err

        res = cls(result.json())

        recursive_defaults(cls.schema, res)

        return res

    call.__name__ = name

    return call


def class_from_schema(name, url, params, schema):
    """
    Creates a AttributeDict subclass that supports dict attribute access.

    The class will have the name passed in, and have the
    other arguments as attributes.
    """
    return type(name, (AttributeDict,), {"url": url, "schema": schema, "params": params})


def recursive_defaults(src, dst):
    for key, value in src.iteritems():
        dst_value = dst.get(key)

        if isinstance(dst_value, dict):
            recursive_defaults(value, dst_value)
        elif not dst_value:
            dst[key] = value() if callable(value) else value
