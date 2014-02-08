tmdb package
============

Documentation of API methods. Most of these are a 1:1 mapping to the TMDB API.

To get started you need an `api_key` from TMDB, please see the TMDB website for such a key.

After you have obtained your `api_key` you can start querying the API from Python by doing
the following simple steps::

    import tmdb
    
    api = tmdb.API(api_key)
    
    results = api.search_movie(query="rocky")
    
    # Do things with results here
    

Notes
-----

- There are several methods currently in the API marked as a `get` request while they
  are actually `post` requests. These do not work currently.
  
- There is currently no caching in the library, it is suggested you do this yourself for now

- There is currently no throttling of requests, it is suggested you do this yourself for now


List of API methods
-------------------
    - :meth:`tmdb.API.configuration`
    - :meth:`tmdb.API.account`
    - :meth:`tmdb.API.account_lists`
    - :meth:`tmdb.API.account_favorite_movies`
    - :meth:`tmdb.API.account_favorite`
    - :meth:`tmdb.API.account_rated_movies`
    - :meth:`tmdb.API.account_movie_watchlist`
    - :meth:`tmdb.API.account_movie_watchlist`
    - :meth:`tmdb.API.authentication_token_new`
    - :meth:`tmdb.API.authentication_session_new`
    - :meth:`tmdb.API.authentication_guest_session_new`
    - :meth:`tmdb.API.certification_movie_list`
    - :meth:`tmdb.API.movie_changes`
    - :meth:`tmdb.API.person_changes`
    - :meth:`tmdb.API.collection`
    - :meth:`tmdb.API.collection_images`
    - :meth:`tmdb.API.company`
    - :meth:`tmdb.API.company_movies`
    - :meth:`tmdb.API.credit`
    - :meth:`tmdb.API.discover_movie`
    - :meth:`tmdb.API.discover_tv`
    - :meth:`tmdb.API.find`
    - :meth:`tmdb.API.genre_list`
    - :meth:`tmdb.API.genre_movies`
    - :meth:`tmdb.API.job_list`
    - :meth:`tmdb.API.keyword`
    - :meth:`tmdb.API.keyword_movies`
    - :meth:`tmdb.API.list`
    - :meth:`tmdb.API.list_item_status`
    - :meth:`tmdb.API.list`
    - :meth:`tmdb.API.list_add_item`
    - :meth:`tmdb.API.list_remove_item`
    - :meth:`tmdb.API.list`
    - :meth:`tmdb.API.movie`
    - :meth:`tmdb.API.movie_alternative_titles`
    - :meth:`tmdb.API.movie_credits`
    - :meth:`tmdb.API.movie_images`
    - :meth:`tmdb.API.movie_keywords`
    - :meth:`tmdb.API.movie_releases`
    - :meth:`tmdb.API.movie_trailers`
    - :meth:`tmdb.API.movie_translations`
    - :meth:`tmdb.API.movie_similar_movies`
    - :meth:`tmdb.API.movie_reviews`
    - :meth:`tmdb.API.movie_lists`
    - :meth:`tmdb.API.movie_changes`
    - :meth:`tmdb.API.movie_latest`
    - :meth:`tmdb.API.movie_upcoming`
    - :meth:`tmdb.API.movie_now_playing`
    - :meth:`tmdb.API.movie_popular`
    - :meth:`tmdb.API.movie_top_rated`
    - :meth:`tmdb.API.movie_account_states`
    - :meth:`tmdb.API.movie_rating`
    - :meth:`tmdb.API.network`
    - :meth:`tmdb.API.person`
    - :meth:`tmdb.API.person_movie_credits`
    - :meth:`tmdb.API.person_tv_credits`
    - :meth:`tmdb.API.person_combined_credits`
    - :meth:`tmdb.API.person_external_ids`
    - :meth:`tmdb.API.person_images`
    - :meth:`tmdb.API.person_changes`
    - :meth:`tmdb.API.person_popular`
    - :meth:`tmdb.API.person_latest`
    - :meth:`tmdb.API.review`
    - :meth:`tmdb.API.search_movie`
    - :meth:`tmdb.API.search_collection`
    - :meth:`tmdb.API.search_tv`
    - :meth:`tmdb.API.search_person`
    - :meth:`tmdb.API.search_list`
    - :meth:`tmdb.API.search_company`
    - :meth:`tmdb.API.search_keyword`
    - :meth:`tmdb.API.tv`
    - :meth:`tmdb.API.tv_credits`
    - :meth:`tmdb.API.tv_external_ids`
    - :meth:`tmdb.API.tv_images`
    - :meth:`tmdb.API.tv_translations`
    - :meth:`tmdb.API.tv_on_the_air`
    - :meth:`tmdb.API.tv_top_rated`
    - :meth:`tmdb.API.tv_popular`
    - :meth:`tmdb.API.tv_season`
    - :meth:`tmdb.API.tv_season_credits`
    - :meth:`tmdb.API.tv_season_external_ids`
    - :meth:`tmdb.API.tv_season_images`
    - :meth:`tmdb.API.tv_season_episode`
    - :meth:`tmdb.API.tv_season_episode_credits`
    - :meth:`tmdb.API.tv_season_episode_external_ids`
    - :meth:`tmdb.API.tv_season_episode_images`

.. autoclass:: tmdb.API
    :members:
    :undoc-members:
    :show-inheritance:
