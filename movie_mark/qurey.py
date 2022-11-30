from .db import get_db
from datetime import datetime

def query_movie_cnt():
    con = get_db()
    cursor = con.cursor()
    cnt = cursor.execute('''
        SELECT count(1) FROM movie
    ''').fetchone()[0]

    return cnt


def query_movie(page, limit=20):
    cnt = query_movie_cnt()
    con = get_db()
    cursor = con.cursor()
    if limit * (page - 1) >= cnt:
        return None
    res = cursor.execute(f'''
        SELECT *
        FROM movie
        LIMIT ? OFFSET ?
    ''', (limit, limit * (page - 1)))

    return res.fetchall()


def query_movie_by_id(movie_id):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
            SELECT *
            FROM movie
            WHERE id=?
        ''', (movie_id,))

    return res.fetchone()


def query_keywords_by_id(movie_id):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                SELECT k.word
                FROM keyword k JOIN has_keyword h ON k.id = h.keyword_id
                JOIN movie m ON m.id = h.movie_id
                WHERE m.id=?
            ''', (movie_id,))

    return res.fetchall()


def query_genres_by_id(movie_id):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                SELECT *
                FROM genre k JOIN is_genre h ON k.id = h.genre_id
                JOIN movie m ON m.id = h.movie_id
                WHERE m.id=?
            ''', (movie_id,))

    return res.fetchall()

def query_director_by_id(movie_id):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                    SELECT p.name
                    FROM movie m JOIN people p ON p.id = m.director_id
                    WHERE m.id=?
                ''', (movie_id,))

    return res.fetchone()[0]

def query_actors_by_id(movie_id):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
        SELECT p.name
        FROM movie m JOIN act_in ai ON m.id = ai.movie_id
        JOIN people p ON ai.actor_id = p.id
        WHERE m.id=?
    ''', (movie_id,))

    return res.fetchall()

def query_like_status_by_id(user_id, movie_id):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
        SELECT COUNT(1)
        FROM like_movie
        WHERE user_id=? AND movie_id=? AND watched=0
    ''', (user_id, movie_id, ))
    added_to_watchlist = res.fetchone()[0] > 0
    res = cursor.execute(f'''
            SELECT COUNT(1)
            FROM like_movie
            WHERE user_id=? AND movie_id=? AND watched=1
        ''', (user_id, movie_id, ))
    added_to_favourite = res.fetchone()[0] > 0
    return added_to_favourite, added_to_watchlist


def query_movie_by_keyword(keyword, page, limit):
    con = get_db()
    cursor = con.cursor()

    res = cursor.execute(f'''
                SELECT *
                FROM movie m JOIN has_keyword hk ON hk.movie_id = m.id
                JOIN keyword k ON k.id = hk.keyword_id
                WHERE k.word LIKE ?
                LIMIT ? OFFSET ?
            ''', (f'%{keyword}%', limit, limit * (page - 1)))
    ret = res.fetchall()
    return len(ret), ret


def query_movie_by_actor(actor, page, limit):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                SELECT *
                FROM movie m JOIN act_in hk ON hk.movie_id = m.id
                JOIN people k ON k.id = hk.actor_id
                WHERE k.name LIKE ?
                LIMIT ? OFFSET ?
            ''', (f'%{actor}%', limit, limit * (page - 1)))
    ret = res.fetchall()
    return len(ret), ret


def query_movie_by_director(director, page, limit):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                SELECT *
                FROM movie m 
                JOIN people k ON k.id = m.director_id
                WHERE k.name LIKE ?
                LIMIT ? OFFSET ?
            ''', (f'%{director}%', limit, limit * (page - 1)))
    ret = res.fetchall()
    return len(ret), ret


def query_movie_by_genre(genre, page, limit):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                SELECT *
                FROM movie m JOIN is_genre hk ON hk.movie_id = m.id
                JOIN genre k ON k.id = hk.genre_id
                WHERE k.genre LIKE ?
                LIMIT ? OFFSET ?
            ''', (f'%{genre}%', limit, limit * (page - 1)))
    ret = res.fetchall()
    return len(ret), ret


def query_movie_by_title(title, page, limit):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                    SELECT *
                    FROM movie m
                    WHERE m.title LIKE ?
                    LIMIT ? OFFSET ?
                ''', (f'%{title}%', limit, limit * (page - 1)))
    ret = res.fetchall()
    return len(ret), ret

def query_watchlist_by_user(user_id, page, limit=21):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
            SELECT m.*, l.save_time
            FROM movie m JOIN like_movie l ON m.id = l.movie_id
            WHERE l.user_id = ? AND l.watched = 0
            LIMIT ? OFFSET ?
        ''', (user_id, limit, limit * (page - 1)))
    ret = res.fetchall()
    return len(ret), ret

def query_favourite_by_user(user_id, page, limit=21):
    con = get_db()
    cursor = con.cursor()
    res = cursor.execute(f'''
                SELECT m.*, l.save_time
                FROM movie m JOIN like_movie l ON m.id = l.movie_id
                WHERE l.user_id = ? AND l.watched = 1
                LIMIT ? OFFSET ?
            ''', (user_id, limit, limit * (page - 1)))

    ret = res.fetchall()
    return len(ret), ret

def like_movie(user_id, movie_id, watched):
    con = get_db()
    cursor = con.cursor()
    cursor.execute(f'''
        INSERT INTO like_movie(user_id, movie_id, watched, save_time)
        VALUES(?, ?, ?, ?)
    ''', (user_id, movie_id, watched, datetime.now()))
    con.commit()

def create_review(user_id, movie_id, content):
    print('!!')
    con = get_db()
    cursor = con.cursor()
    cursor.execute(f'''
        INSERT INTO review(user_id, movie_id, content, post_time)
        VALUES(?, ?, ?, ?)
    ''', (user_id, movie_id, content, datetime.now()))
    con.commit()

def query_review_by_movie(movie_id):
    cursor = get_db().cursor()
    res = cursor.execute(f'''
        SELECT r.*, u.username
        FROM review r
        JOIN user u ON u.id=r.user_id
        WHERE movie_id=?
    ''', (movie_id, ))
    return res.fetchall()


