from __future__ import unicode_literals
import re
import json
import pprint

from bs4 import BeautifulSoup

try: # PY2
    from StringIO import StringIO
except ImportError: # PY3
    from io import StringIO

try:
    str = unicode
except NameError:
    str = str


api_documentation_url = "http://docs.themoviedb.apiary.io/"

start_template = """from __future__ import unicode_literals, absolute_import
from .mani import schema
from .api import create_endpoint

try:
    str = unicode
except NameError:
    str = str
"""

param_template = """
    :param {type:s} {name:s}: {description:s}
"""

doc_template = """For more information on return value see official API docs {permalink:s}

For information about possible exceptions see :mod:`tmdb.errors` documentation.

{required_parameters:s}

{optional_parameters:s}

Usage:
    >>> api = tmdb.API(api_key)
    >>> api.{method_name:s}(<parameters>)
    {example_output:s}
"""

endpoint_template = """
create_endpoint(
    docs={docstring:s},
    url={url:s},
    class_name={class_name:s},
    method_name={method_name:s},
    schema=schema({example:s}),
    parameters={params:s},
)
"""


def generate_param_docstring(params):
    result = []
    for name, type in params.items():
        description = ""
        if isinstance(type, tuple):
            type, description = type
            # Get rid of the description in the parameter dict
            params[name] = type

        res = param_template.format(type=repr(type), name=name, description=description)

        # Only strip newlines, indentation should be kept intact
        res = res.strip("\n")

        result.append(res)

    return "\n".join(result)


def generate_docstring(endpoint, permalink):
    # Get param docs
    doc_req_param = generate_param_docstring(endpoint["params"].get("required", {}))
    doc_opt_param = generate_param_docstring(endpoint["params"].get("optional", {}))

    # only add them if we have any
    if doc_req_param:
        doc_req_param = "Required Parameters\n" + doc_req_param
    if doc_opt_param:
        doc_opt_param = "Optional Parameters\n" + doc_opt_param


    # Generate a pretty printed example result
    buffer = StringIO()

    pprint.pprint(endpoint['example'], stream=buffer)

    example = buffer.getvalue()

    # Fix an indentation problem with pprint and our example
    example = example.replace("\n", "\n    ")

    return doc_template.format(
        permalink=permalink,
        method_name=endpoint["method_name"],
        example_output=example,
        required_parameters=doc_req_param,
        optional_parameters=doc_opt_param,
    )


def generate_method_name(url):
    # Get rid of any version number
    url = url.lstrip("/3/")

    # We don't want parameter names in the method name, remove them
    url = re.sub(r"/{.*?}", "", url)

    # And then just replace any leftover slashes by an underscore
    return url.replace("/", "_")


def generate_class_name(url):
    # We can use the method name as base for the class name
    method_name = generate_method_name(url)

    # Straightforward capitalization for the class name
    parts = [part.capitalize() for part in method_name.split("_")]

    return "".join(parts)


class Type(object):
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return as_usable(self.type)


def as_usable(type):
    """
    Returns a type representation for in documentation
    """
    if type == int:
        return "int"
    elif type == str:
        return "str"
    return "str"

def guess_type(name):
    """
    Guess the type by the parameter name, defaults to unicode
    """
    if name in ("id", "page"):
        return Type(int)
    elif "number" in name:
        return Type(int)
    elif "date" in name:
        # TODO: Make this support date/time
        return Type(str)
    else:
        return Type(str)

def main(output_file, html):
    soup = BeautifulSoup(html)

    resources = soup.find_all(class_="resource")

    # Find all the API urls
    urls = [s.hgroup.h2.text for s in resources]

    # Permalinks for linking in documentation
    permalinks = [api_documentation_url + s.get('href') for s in soup.find_all(class_="resourcePermalink")]

    # Extract API parameters
    tables = [s.table for s in resources]

    params = []
    for url, table in zip(urls, tables):
        parameters = {}
        order = []

        # Get out any required parameters from the url
        for required in re.findall(r"{(.*?)}", url):
            value = parameters.get("required", {})

            order.append(required)
            value[required] = guess_type(required)

            parameters["required"] = value

        if order:
            parameters["order"] = order

        # Remember what key we're filling, optional or required
        key = None
        for row in table.find_all("tr"):
            first = True
            for td in row.find_all("td"):
                content = td.text

                if content == "api_key":
                    continue

                # Parameter has a description with it, so save it somewhere
                if not first:
                    parameters[key][param] = (parameters[key][param], content)
                    # Make sure we don't loop a third time for some reason
                    break

                if content.lower() == "required parameters":
                    key = "required"
                elif content.lower() == "optional parameters":
                    key = "optional"
                elif key:
                    value = parameters.get(key, {})

                    value[content] = guess_type(content)

                    parameters[key] = value

                    first = False
                param = content

        params.append(parameters)

    schemas = []
    # Extract all the API response examples for schema parsing
    for example in soup.find_all(class_="language-javascript"):
        response = json.loads(example.text)

        schemas.append(response)


    print len(urls), len(params), len(schemas)

    result = []
    for url, permalink, schema, param in zip(urls, permalinks, schemas, params):
        d = {
            "url": url,
            "class_name": generate_class_name(url),
            "method_name": generate_method_name(url),
            "example": schema,
            "params": param,
        }

        # This also removes any leftover tuples we used for
        # parameter descriptions in params
        d["docstring"] = generate_docstring(d, permalink)

        result.append(d)


    # Now write everything to a python script for usage by the module
    f = open(output_file, "wb")

    f.write(start_template)

    for r in result:
        d = {}
        for key, item in r.items():
            d[key] = repr(item)

        call = endpoint_template.format(**d)
        f.write(call)

    f.close()
