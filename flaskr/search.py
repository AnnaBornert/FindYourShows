from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from flaskr.backend import *
from flaskr.classes import *

bp = Blueprint('search', __name__)


@bp.route('/', methods=('GET', 'POST'))
def search():
    """
    Renders the search.html template if it is a GET request and the redirects to the get_results view if it is a POST
    """
    if request.method == 'POST':
        title = request.form['title']
        error = None
        genres_id = []
        genres_names = ""
        if request.form.get("action & adventure"):
            genres_id.append("10759")
            genres_names += "action & adventure "
        if request.form.get("animation"):
            genres_id.append("16")
            genres_names += "animation "
        if request.form.get("comedy"):
            genres_id.append("35")
            genres_names += "comedy "
        if request.form.get("crime"):
            genres_id.append("80")
            genres_names += "crime "
        if request.form.get("documentary"):
            genres_id.append("99")
            genres_names += "documentary "
        if request.form.get("drama"):
            genres_id.append("18")
            genres_names += "drama "
        if request.form.get("family"):
            genres_id.append("10751")
            genres_names += "family "
        if request.form.get("kids"):
            genres_id.append("10762")
            genres_names += "kids "
        if request.form.get("mystery"):
            genres_id.append("9648")
            genres_names += "mystery "
        if request.form.get("news"):
            genres_id.append("10763")
            genres_names += "news "
        if request.form.get("reality"):
            genres_id.append("10764")
            genres_names += "reality "
        if request.form.get("sci-fi & fantasy"):
            genres_id.append("10765")
            genres_names += "sci-fi & fantasy "
        if request.form.get("soap"):
            genres_id.append("10766")
            genres_names += "soap "
        if request.form.get("talk"):
            genres_id.append("10767")
            genres_names += "talk "
        if request.form.get("war & politics"):
            genres_id.append("10768")
            genres_names += "war & politics "
        if request.form.get("western"):
            genres_id.append("37")
            genres_names += "western "
        genres = genre_str(genres_id)

        if not title and not genres:
            error = 'A TV myshow name is required.'

        if error is not None:
            flash(error)
        elif not title:
            return redirect(url_for('search.get_results_genres', genres=genres, genres_names=genres_names))
        else:
            return redirect(url_for('search.get_results', query=title))

    # add/update logged in user's myshow ids to its session
    shows_to_session()

    if ('user_id' in session) and (len(session['show_ids']) > 0):
        last_show_id = session['show_ids'][-1]
        try:
            shows, total_pages = get_shows_from_search(None, kind='recommendation', show_id=last_show_id)
        # We handle exceptions when the API is not working as we expect
        except APIError as error:
            print(error)
            return redirect(url_for('error'))
        except KeyError as error:
            print('ERROR The following field must have been removed from the API : ' + str(error))
            return redirect(url_for('error'))
        except TypeError as error:
            print('ERROR The following field must have been modified in the API : ' + str(error))
            return redirect(url_for('error'))
        session['last_show_name'] = ShowDetailedView(last_show_id).title
        return render_template('search/search.html', shows=shows)

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='trending_day')
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/search.html', shows=shows)


@bp.route('/results/<query>', defaults={'page': 1}, methods=('GET', 'POST'))
@bp.route('/results/<query>/<int:page>', methods=('GET', 'POST'))
def get_results(query, page):
    """
    Renders the results.html template if it is a GET request with the result of the search query and redirects to the
    get_results view if it is a POST
    """
    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'A TV myshow name is required.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search.get_results', query=title))

    # add/update logged in user's myshow ids to its session
    shows_to_session()

    if query is None:
        query = 'house'

    try:
        shows, total_pages = get_shows_from_search(query, page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        raise APIError(error)
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/results.html', shows=shows, current_page=page, total_pages=total_pages, query=query)


@bp.route('/results_genres/<genres>/<genres_names>', defaults={'page': 1}, methods=('GET', 'POST'))
@bp.route('/results_genres/<genres>/<genres_names>/<int:page>', methods=('GET', 'POST'))
def get_results_genres(genres, genres_names, page):
    """
    Renders the results_genres.html template if it is a GET request with the result of the search genres and redirects to the
    get_results_genres view if it is a POST
    """
    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'A TV myshow name is required.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search.get_results', query=title))


    # add/update logged in user's myshow ids to its session
    shows_to_session()

    try:
        shows, total_pages = get_shows_from_search(None, kind='discover', genres=genres, page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        raise APIError(error)
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/results_genres.html', shows=shows, current_page=page, total_pages=total_pages, genres=genres, genres_names=genres_names)

@bp.route('/trending', defaults={'page': 1})
@bp.route('/trending/<int:page>', methods=('GET',))
def get_trending(page):
    """
    Renders the week's trends page
    """

    # add/update logged in user's myshow ids to its session
    shows_to_session()

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='trending_week', page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))


    return render_template('search/trending.html', shows=shows, current_page=page, total_pages=total_pages)


@bp.route('/popular', defaults={'page': 1})
@bp.route('/popular/<int:page>', methods=('GET',))
def get_popular(page):
    """
    Renders the popular tv shows page
    """

    # add/update logged in user's myshow ids to its session
    shows_to_session()

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='popular', page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/popular.html', shows=shows, current_page=page, total_pages=total_pages)


@bp.route('/top_rated', defaults={'page': 1})
@bp.route('/top_rated/<int:page>', methods=('GET',))
def get_top_rated(page):
    """
    Renders the top rated tv shows page
    """

    # add/update logged in user's myshow ids to its session
    shows_to_session()

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='top_rated', page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/top_rated.html', shows=shows, current_page=page, total_pages=total_pages)




