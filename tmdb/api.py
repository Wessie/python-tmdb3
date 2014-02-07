import requests


class TMDBError(Exception):
    pass


class API(object):
    base_url = "https://api.themoviedb.org"
    def __init__(self, api_key):
        super(API, self).__init__()

        self.key = api_key

    @classmethod
    def register(cls, name, schema_cls):
        """
        Creates a method on the API class with name `name`.

        :param name: name of the method, will overwrite if already exists
        :param schema_cls: class as returned by `class_from_schema`.
        """
        setattr(cls, name, create_api_method(name, schema_cls))


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
            return super(AttributeDict, self).__getattr__(key)

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


def create_api_method(name, cls):
    """
    Creates a method for the API class based on the class passed in.

    The method will have name `name` and will return values of type `cls`.
    """
    def call(api, *positional, **params):
        # Check for positional arguments and convert them to key arguments by
        # use of `params.order` or raise exception if incorrect.
        positional_order = cls.params.get("order", [])

        if len(positional) > len(positional_order):
            raise ValueError(
                "Got too many positional arguments, got %d expected "
                "maximum of %d" % (len(positional), len(positional_order))
            )

        for key, value in zip(positional_order, positional):
            params[key] = value

        # Check for parameters we don't know
        for key in params:
            if key not in cls.params_all:
                raise ValueError("Function '%s' does not take argument '%s'" % (name, key))

        # Check for all required arguments
        for key in cls.params_required:
            if key not in params:
                raise ValueError("Function '%s' missing required argument '%s'" % (name, key))


        # We've checked out all the validation
        url = cls.url.format(**params)
        url = api.base_url + url

        params['api_key'] = api.key

        try:
            result = requests.get(url, params=params)
            result.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise err

        res = cls(result.json())

        # Add any defaults for missing keys
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
    # Create a dict of both parameters, for easy access later
    all = {}
    all.update(params.get("required", {}))
    all.update(params.get("optional", {}))

    return type(name, (AttributeDict,), {
        "url": url,
        "schema": schema,
        "params": params,
        "params_all": all,
        "params_required": params.get("required", {})
    })


def create_endpoint(url, class_name, method_name, schema, parameters):
    if isinstance(method_name, unicode):
        method_name = method_name.encode("utf8")
    if isinstance(class_name, unicode):
        class_name = class_name.encode("utf8")

    cls = class_from_schema(class_name, url, parameters, schema)
    API.register(method_name, cls)


def recursive_defaults(src, dst):
    for key, value in src.iteritems():
        dst_value = dst.get(key)

        if isinstance(dst_value, dict):
            recursive_defaults(value, dst_value)
        elif not dst_value:
            dst[key] = value() if callable(value) else value
