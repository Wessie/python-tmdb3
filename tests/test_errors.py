import pytest

import tmdb


def test_tmdb_error():
    error = tmdb.TMDBError({"message": "a test"})

    assert error.message == "a test"


def test_tmdb_api_error():
    error = tmdb.APIError({"status_message": "a test", "status_code": 7})

    assert error.message == "a test"
    assert error.status == 7
