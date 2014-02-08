from __future__ import unicode_literals
from __future__ import absolute_import
from .util import AttributeDict


class TMDBError(Exception):
    """
    Base Exception of the TMDB API, all other
    exceptions inherit from this.

    attributes:
        message: Human readable error message
    """
    def __init__(self, message):
        for key, value in message.items():
            setattr(self, key, value)


class LibraryError(TMDBError):
    """
    Exception that should only occur if there is
    a code error in the library, please report
    an issue with the full traceback if this exception
    happens.
    """


class NetworkError(TMDBError):
    """
    Exception that occurs if we could not reach the
    TMDB API with our request. Indicates TMDB or
    your connection is down.
    """


class InvalidResponseError(TMDBError):
    """
    Exception that occurs when a request to the API nets
    an invalid response. This is a TMDB API issue if it
    occurs.
    """


class TimeoutError(TMDBError):
    """
    Exception that occurs when a request to the API reaches
    the timeout set in the API instance.

    This might mean the TMDB API is down and/or slow.
    """


class APIError(TMDBError):
    """
    Exception that indicates the error came from the API,
    rather than from the request and/or library.

    This is a baseclass for other exceptions but will also
    be raised itself when an unknown API error occurs.

    attributes:
        message: Human readable error message returned by the TMDB API
        status: A status code returned by the TMDB API
    """
    def __init__(self, message):
        # Edit response
        if "status_message" in message:
            message["message"] = message["status_message"]
            del json["status_message"]
        if "status_code" in message:
            message["status"] = message["status_code"]
            del message["status_code"]

        super(APIError, self).__init__(json)


class DoesNotExist(APIError):
    """
    Exception that occurs when a resource does not
    exist when requested. e.g. non-existant id parameter.
    """


class APIKeyError(APIError):
    """
    Exception that occurs when your API key used in the
    request is invalid.
    """


class ThrottlingError(APIError):
    """
    Exception that occurs when you hit the request/s limit
    set by the TMDB server. See the API documentation for
    the limits estiablished by TMDB.
    """
