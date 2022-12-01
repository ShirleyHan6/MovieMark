from flask import Blueprint, render_template, request, redirect, url_for, g
from .qurey import query_movie, query_movie_cnt, query_movie_by_id, query_genres_by_id, query_keywords_by_id,\
    query_actors_by_id, query_movie_by_actor, query_movie_by_genre, query_movie_by_keyword, query_movie_by_director, \
    query_movie_by_title, query_director_by_id, like_movie, query_like_status_by_id, query_watchlist_by_user, \
    query_favourite_by_user, create_review, query_review_by_movie
from .auth import login_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 21))
    movies = query_movie(page, limit)
    cnt = query_movie_cnt()
    return render_template('index.html', movies=movies, page=page, max_page=cnt / limit + 1)

@login_required
@main_bp.route('/detail', methods=['GET', 'POST'])
def detail():
    if 'movie_id' not in request.args:
        return redirect(url_for('main.index'))
    movie_id = int(request.args.get('movie_id'))
    if request.method == 'POST':
        content = request.form['review']
        create_review(g.user['id'], movie_id, content)

    reviews = query_review_by_movie(movie_id)
    movie = query_movie_by_id(movie_id)
    keywords = query_keywords_by_id(movie_id)
    actors = query_actors_by_id(movie_id)
    # print(movie_id)
    genres = query_genres_by_id(movie_id)
    director = query_director_by_id(movie_id)
    added_to_favourite, added_to_watchlist = query_like_status_by_id(g.user['id'], movie_id)
    # print(added_to_favourite, added_to_watchlist)
    return render_template('movie_detail.html', movie=movie, genres=genres, keywords=keywords, actors=actors,
                           director=director, added_to_watchlist=added_to_watchlist,
                           added_to_favourite=added_to_favourite, reviews=reviews)

@main_bp.route('/search', methods=['GET'])
def search():
    if 'q' not in request.args or 't' not in request.args:
        return redirect(url_for('main.index'))
    q = request.args.get('q')
    t = request.args.get('t')
    if not q or not t:
        return redirect(url_for('main.index'))
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 21))
    cnt = 0
    if t == 'actor':
        cnt, movies = query_movie_by_actor(q, page, limit)
    elif t == 'title':
        cnt, movies = query_movie_by_title(q, page, limit)
    elif t == 'director':
        cnt, movies = query_movie_by_director(q, page, limit)
    elif t == 'keyword':
        cnt, movies = query_movie_by_keyword(q, page, limit)
    elif t == 'genre':
        cnt, movies = query_movie_by_genre(q, page, limit)
    else:
        return redirect(url_for('main.index'))

    return render_template('search_result.html', movies=movies, page=page, max_page=cnt / limit + 1, q=q, t=t)

@login_required
@main_bp.route('/add_to_watchlist', methods=['GET'])
def add_to_watchlist():
    if 'movie_id' not in request.args:
        return '', 200

    movie_id = request.args.get('movie_id')
    # print(g.user)
    like_movie(g.user['id'], movie_id, 0)
    return '', 200

@login_required
@main_bp.route('/add_to_favourite', methods=['GET'])
def add_to_favourite():
    if 'movie_id' not in request.args:
        return '', 200
    movie_id = request.args.get('movie_id')
    like_movie(g.user['id'], movie_id, 1)
    return '', 200

@login_required
@main_bp.route('/watchlist', methods=['GET'])
def watchlist():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 21))
    user_id = g.user['id']
    cnt, movies = query_watchlist_by_user(user_id, page, limit)
    return render_template('watchlist.html', movies=movies, page=page, max_page=cnt / limit + 1)

@login_required
@main_bp.route('/favourite', methods=['GET'])
def favourite():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 21))
    user_id = g.user['id']
    cnt, movies = query_favourite_by_user(user_id, page, limit)
    return render_template('watchlist.html', movies=movies, page=page, max_page=cnt / limit + 1)