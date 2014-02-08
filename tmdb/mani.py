from __future__ import unicode_literals
import logging
import itertools


logger = logging.getLogger(__name__)
DEFAULT = object()


def validate(obj, sch):
    """
    Compares an obj to a schema, returns bool
    """
    return schema(obj) == sch


def apply(obj, sch):
    """
    Apply a schema to an object, raises an exception if schema can't
    be forced upon the object.
    """
    if obj is type or sch is type:
        raise TypeError("Found absolute 'type' in schema or object.")

    if obj is DEFAULT:
        obj = sch() if isinstance(sch, type) else type(sch)()

    if isinstance(sch, dict) and isinstance(obj, dict):
        return {key: apply(obj.get(key, DEFAULT), value_sch) for key, value_sch in sch.items()}
    elif isinstance(sch, list) and isinstance(obj, list):
        # Unbounded lists should loop forever in the applying case
        if isinstance(sch, UnboundedList):
            it = itertools.cycle(sch)
        else:
            it = sch

        return [apply(value, value_sch) for value, value_sch in zip(obj, it)]

    if obj is not None and isinstance(obj, sch):
        return obj
    elif sch is Any:
        # TODO: Fix this?
        # Accept literally anything
        return obj
    else:
        logger.warning("Schema mismatch, discarding object %r" % obj)
        return sch()


def schema(obj):
    """
    Returns the type (according to this module) of an object
    """
    if isinstance(obj, dict):
        return {key: schema(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        result = [schema(item) for item in obj]

        if result:
            # If all the items are the same, we assume there is no set length for the list
            first = result[0]

            result = UnboundedList(result) if all(first == item for item in result) else result
        else:
            # An empty list? Replace it with an Any because empty lists don't exist in a schema
            result = Any

        return result
    elif obj is None:
        return Any

    return type(obj)


class UnboundedList(list):
    """
    Indicates a list has no set length in the schema
    """
    def __init__(self, initial=None):
        leftover = initial = initial or []
        final = {}

        for schema in initial:
            if not isinstance(schema, dict):
                break

            for key, type in schema.items():
                if key not in final:
                    final[key] = type
                elif key in final and final[key] is Any:
                    final[key] = type
                elif final[key] == type:
                    continue
                else:
                    print("SHIT BROKE")
        else:
            leftover = [final]

        super(UnboundedList, self).__init__(leftover)

    def __eq__(self, other):
        if isinstance(other, list) and len(other) == 0:
            return True
        return super(UnboundedList, self).__eq__(other)


class Any(object):
    def __eq__(self, other):
        return True

Any = Any()
