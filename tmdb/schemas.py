from .api import API, class_from_schema


movie_schema = {
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
}
