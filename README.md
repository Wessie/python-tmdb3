python-tmdb3
============

[![Build Status](https://travis-ci.org/Wessie/python-tmdb3.png?branch=master)](https://travis-ci.org/Wessie/python-tmdb3)
[![Coverage Status](https://coveralls.io/repos/Wessie/python-tmdb3/badge.png?branch=master)](https://coveralls.io/r/Wessie/python-tmdb3?branch=master)

Light Python API around TheMovieDB API version 3, which the documentation off is [here](http://docs.themoviedb.apiary.io/)

The following Python versions are supported: `Python 2.6`, `Python 2.7`, `Python 3.3+`, `PyPy`


Examples
========

Receive information by movie ID
```python
>>> import tmdb
>>> api = tmdb.API(your_api_key)
>>> api.movie(550)
```

Search for movies:
```python
>>> import tmdb
>>> api = tmdb.API(your_api_key)
>>> api.search_movie(query="Rocky")
```

And many more, for all available methods see (for now as documentation isn't setup yet) `dir(tmdb.API)`.
