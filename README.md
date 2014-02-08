python-tmdb3
============

[![Build Status](https://travis-ci.org/Wessie/python-tmdb3.png?branch=master)](https://travis-ci.org/Wessie/python-tmdb3)
[![Coverage Status](https://coveralls.io/repos/Wessie/python-tmdb3/badge.png?branch=master)](https://coveralls.io/r/Wessie/python-tmdb3?branch=master)

Light Python API around TheMovieDB API version 3, which the documentation off is [here](http://docs.themoviedb.apiary.io/)

The following Python versions are supported: `Python 2.6`, `Python 2.7`, `Python 3.3+`, `PyPy`


Installation
============

Currently, `python-tmdb3` is not on `pip`. To install you can use the following `pip` command for now:

`pip install -e git+https://github.com/Wessie/python-tmdb3.git#egg=tmdb`


Examples
========

Create an API instance:
```python
>>> import tmdb
>>> api = tmdb.API(your_api_key)
```

Receive information by movie ID
```python
>>> api.movie(550)
```

Search for movies:
```python
>>> api.search_movie(query="Rocky")
```

And many more (a total of 86 methods), for all available methods see (for now as documentation isn't setup yet) `dir(tmdb.API)`.


Issues
======

Most of the code is auto-generated, and most likely not perfect. Please file an issue if you run into
a problem using `python-tmdb3`.
