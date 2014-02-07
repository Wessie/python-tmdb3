from __future__ import unicode_literals
from . import api


api.create_endpoint(
    url="/3/movie/{id:d}",
    class_name="Movie",
    method_name="movie",
    schema={
        "adult": bool,
        "backdrop_path": unicode,
        "belongs_to_collection": bool,
        "budget": int,
        "genres": list,
        "homepage": unicode,
        "id": int,
        "imdb_id": unicode,
        "original_title": unicode,
        "overview": unicode,
        "popularity": float,
        "poster_path": unicode,
        "production_companies": list,
        "production_countries": list,
        "release_date": unicode,
        "revenue": int,
        "runtime": int,
        "spoken_languages": list,
        "status": unicode,
        "tagline": unicode,
        "title": unicode,
        "vote_average": float,
        "vote_count": int,
    },
    parameters={
        "required": {"id": int},
        "optional": {"language": unicode},
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/alternative_titles",
    class_name="MovieAlternativeTitles",
    method_name="movie_alt_titles",
    schema={
        "id": int,
        "titles": list,
    },
    parameters={
        "required": {"id": int},
        "optional": {"country": unicode},
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/credits",
    class_name="MovieCredits",
    method_name="movie_credits",
    schema={
        "id": int,
        "cast": list,
        "crew": list,
    },
    parameters={
        "required": {"id": int},
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/images",
    class_name="MovieImages",
    method_name="movie_images",
    schema={
        "id": int,
        "backdrops": list,
        "posters": list,
    },
    parameters={
        "required": {"id": int},
        "optional": {
            "language": unicode,
            "include_image_language": list,
        },
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/keywords",
    class_name="MovieKeywords",
    method_name="movie_keywords",
    schema={
        "id": int,
        "keywords": list,
    },
    parameters={
        "required": {"id": int},
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/releases",
    class_name="MovieReleases",
    method_name="movie_releases",
    schema={
        "id": int,
        "countries": list,
    },
    parameters={
        "required": {"id": int},
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/trailers",
    class_name="MovieTrailers",
    method_name="movie_trailers",
    schema={
        "id": int,
        "quicktime": list,
        "youtube": list,
    },
    parameters={
        "required": {"id": int},
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/translations",
    class_name="MovieTranslations",
    method_name="movie_translations",
    schema={
        "id": int,
        "translations": list,
    },
    parameters={
        "required": {"id": int},
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/similar_movies",
    class_name="MovieSimilar",
    method_name="movie_similar",
    schema={
        "page": int,
        "results": list,
        "total_pages": int,
        "total_results": int,
    },
    parameters={
        "required": {"id": int},
        "optional": {
            "page": int,
            "language": unicode,
        },
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/reviews",
    class_name="MovieReviews",
    method_name="movie_reviews",
    schema={
        "id": int,
        "page": int,
        "results": list,
        "total_pages": int,
        "total_results": int,
    },
    parameters={
        "required": {"id": int},
        "optional": {
            "page": int,
            "language": unicode,
        },
        "order": ["id"],
    },
)

api.create_endpoint(
    url="/3/movie/{id:d}/lists",
    class_name="MovieLists",
    method_name="movie_lists",
    schema={
        "id": int,
        "page": int,
        "results": list,
        "total_pages": int,
        "total_results": int,
    },
    parameters={
        "required": {"id": int},
        "optional": {
            "page": int,
            "language": unicode,
        },
        "order": ["id"],
    },
)
