from __future__ import unicode_literals
import requests

from . import mani
from . import errors
from .util import AttributeDict


# py2/3 compat
try:
    str = unicode
    PY3 = False
except NameError:
    PY3 = True
    str = str


class API(object):
    base_url = "https://api.themoviedb.org"
    def __init__(self, api_key):
        super(API, self).__init__()

        self.key = api_key

    @classmethod
    def register(cls, name, schema_cls, docs=""):
        """
        Creates a method on the API class with name `name`.

        :param name: name of the method, will overwrite if already exists
        :param schema_cls: class as returned by `class_from_schema`.
        """
        setattr(cls, name, create_api_method(name, schema_cls, docs=docs))


class BaseResult(object):
    schema = {}
    def __init__(self, dct):
        dct = mani.apply(dct, self.schema)

        super(BaseResult, self).__init__(dct)


def create_api_method(name, cls, docs=""):
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
        except requests.exceptions.ConnectionError as err:
            raise errors.NetworkError({
                "message": "Failed to connect to API, please check your connection",
            })
        except requests.exceptions.HTTPError as err:
            raise errors.InvalidResponseError({
                "message": "Response from API is an invalid HTTP response"
            })
        except requests.exceptions.Timeout as err:
            raise errors.TimeoutError({
                "message": "Request took too long to complete",
            })
        except requests.exceptions.TooManyRedirects as err:
            raise errors.InvalidResponseError({
                "message": "Response from API had too many redirects in chain",
            })

        # If all is well, get ourself out of here
        if result.status_code == requests.codes.ok:
            return cls(result.json())

        # Else... well that wasn't a success, clean up~
        if result.status_code == requests.codes.not_found and result.content == b"<h1>Not Found</h1>":
            raise errors.LibraryError({
                "message": "Requested resource does not exist",
            })
        elif result.status_code == requests.codes.not_found:
            raise errors.DoesNotExist(result.json())
        elif result.status_code == requests.codes.unauthorized:
            raise errors.APIKeyError(result.json())
        elif result.status_code == requests.codes.unavailable:
            raise errors.ThrottlingError(result.json())

        # Not a clue, lack of documentation in the API docs
        try:
            message = result.json()
        except:
            message = {"message": "Unknown error: %s" % result.text}

        raise errors.APIError(message)

    call.__name__ = name
    call.__doc__  = docs

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

    if isinstance(name, str) and not PY3:
        name = name.encode("utf8")

    return type(name, (BaseResult, AttributeDict), {
        "url": url,
        "schema": schema,
        "params": params,
        "params_all": all,
        "params_required": params.get("required", {})
    })


def create_endpoint(url, class_name, method_name, schema, parameters, docs=""):
    if isinstance(method_name, str) and not PY3:
        method_name = method_name.encode("utf8")
    if isinstance(class_name, str) and not PY3:
        class_name = class_name.encode("utf8")

    cls = class_from_schema(class_name, url, parameters, schema)
    API.register(method_name, cls, docs=docs)


def recursive_defaults(src, dst):
    """
    Recursively goes through keys in src and checks if `key in dst` is True.
    If the key does not exist, src[key] is called to provide a default
    value.
    """
    for key, value in src.items():
        dst_value = dst.get(key)

        if isinstance(dst_value, dict):
            recursive_defaults(value, dst_value)
        elif not dst_value:
            dst[key] = value() if callable(value) else value
