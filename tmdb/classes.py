from .api import API, class_from_schema
from .schemas import *


parameters = {"required": {"id": int}, "optional": {"language": unicode}}
Movie = class_from_schema("Movie", "https://api.themoviedb.org/3/movie/{id:d}",
                          parameters, movie_schema)
API.register("movie", Movie)
