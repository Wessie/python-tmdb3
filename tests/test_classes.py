from __future__ import unicode_literals

import tmdb

import pytest

@pytest.fixture
def schema():
    return {
        "id": int,
        "test": list,
        "string": unicode,
        "date": unicode,
    }


def test_class_creation(schema):
    cls = tmdb.api.class_from_schema(
        name="test",
        url="testurl",
        params={},
        schema=schema,
    )

    assert cls.url == "testurl"
    assert cls.params == {}
    assert cls.schema == schema
    assert cls.__name__ == "test"


def test_class_behaviour(schema):
    cls = tmdb.api.class_from_schema(
        name="test",
        url="testurl",
        params={},
        schema=schema,
    )

    inst = cls({"date": "test"})

    # Attribute access and default value test
    assert inst.id == 0
    assert inst.test == []
    assert inst.string == ""
    assert inst.date == "test"
