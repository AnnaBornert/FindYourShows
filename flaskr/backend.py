from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

import requests, werkzeug
from flaskr.db import get_db
from flaskr.classes import *

# Parameters that are used several times in the code below
api_path = 'https://api.themoviedb.org/3/'
params = {'api_key': 'df7d8e0359122d2f3e6348064a104074'}


def get_shows_from_search(query, kind='search_query', genres=None, show_id=None, page=1):
    """
    This function handles the different API calls and returns the results.
    The different API calls have to be specified in the 'kind' parameter, possibilities are : 'search_query' (default),
    'trending_day','trending_week','popular','top_rated','recommendation'
    All the results are stored in Show objects (cf classes.py).
    """
    params['page'] = page

    if kind == 'search_query':
        params['query'] = query
        req = requests.get(api_path + 'search/tv', params)
    elif kind == 'trending_day':
        # Get the list of today's trending shows with an API call
        req = requests.get(api_path + 'trending/tv/day', params)
    elif kind == 'trending_week':
        # Get the list of today's trending shows with an API call
        req = requests.get(api_path + 'trending/tv/week', params)
    elif kind == 'popular':
        req = requests.get(api_path + 'tv/popular', params)
    elif kind == 'top_rated':
        req = requests.get(api_path + 'tv/top_rated', params)
    elif kind == 'recommendation' and show_id is not None:
        req = requests.get(api_path + 'tv/' + str(show_id) + '/recommendations', params)
    elif kind == 'discover' and genres is not None:
        params['with_genres'] = genres
        req = requests.get(api_path + 'discover/tv', params)
    else:
        print('Please enter a correct request type.')

    # Check the response status code and raise a custom exception if not 200
    if not req.ok:
        raise APIError(req.status_code)

    req_json = req.json()

    results = []
    if req_json["total_results"] == 0:
        flash("No results were found for your search.")

    for res in req_json["results"]:
        results += [Show(res)]

    return results, req_json["total_pages"]


def shows_to_session():

    if 'user_id' not in session:
        return None

    shows = []
    show_ids = get_db().execute(
        'SELECT show_id'
        ' FROM shows_users '
        ' WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()

    for show in show_ids:
        shows += [show['show_id']]

    session['show_ids'] = shows
    return None

#utile?

def make_multi_requests(show_ids):


    # lets make the new shows appear first
    temp = []
    for i in range(len(show_ids)):
        temp.append(show_ids[-(i+1)])
    show_ids = temp

    # lets launch all the API call threads
    APIrequest.initiate()
    APIrequest.show_ids = show_ids
    threads = []
    for i in show_ids:
        threads.append(APIrequest())

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    results = [0] * len(show_ids)

    # we reorder the results
    for show_id in APIrequest.shows.keys():
        results[show_ids.index(show_id)] = APIrequest.shows[show_id]

    return results


def genre_str(genre):
    if len(genre) == 0:
        return None
    elif len(genre) == 1:
        return genre[0]
    else:
        genres = genre[0]
        for i in range(1, len(genre)):
            genres = genres + ", "
            genres = genres + genre[i]
        return genres





