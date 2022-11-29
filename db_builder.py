import os.path
import requests
from http import HTTPStatus
import pandas as pd
import sqlite3

DATABASE_URL = './movie_mark/movie.sqlite'


class DBConnection:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = connect_db()
        return self.connection

    def get_cursor(self):
        return self.get_connection().cursor()


db_connection = DBConnection()


def connect_db():
    """
    :return: connection
    """
    return sqlite3.connect(
        DATABASE_URL,
        detect_types=sqlite3.PARSE_DECLTYPES
    )


def build_schema():
    if not os.path.exists(DATABASE_URL):
        connect = db_connection.get_connection()
        with open('./schema.sql') as f_p:
            print('execute script')
            connect.executescript(f_p.read())
        connect.commit()
    delete_all()


def get_director_or_actor_id(name):
    cursor = db_connection.get_cursor()
    res = cursor.execute(f'''
            SELECT id
            FROM people
            WHERE name = ?
        ''', (name,))
    p_id = res.fetchone()
    if p_id is None:
        return -1
    return p_id[0]


def get_genre_id(genre):
    cursor = db_connection.get_cursor()
    res = cursor.execute(f'''
        SELECT id
        FROM genre
        WHERE genre = ?
    ''', (genre,))
    genre_id = res.fetchone()
    if not genre_id:
        return -1
    return genre_id[0]

def get_keyword_id(keyword):
    cursor = db_connection.get_cursor()
    res = cursor.execute(f'''
            SELECT id
            FROM keyword
            WHERE word = ?
        ''', (keyword,))
    genre_id = res.fetchone()
    if not genre_id:
        return -1
    return genre_id[0]

def get_movie_id(movie):
    cursor = db_connection.get_cursor()
    # print(movie['title'], movie['year'], get_director_or_actor_id(movie['director_id']))
    res = cursor.execute(f'''
        SELECT id
        FROM movie
        WHERE title = ? AND year = ? AND director_id = ?
    ''', (movie['title'], movie['year'], movie['director_id']))
    movie_id = res.fetchone()
    if movie_id is None:
        return -1
    return movie_id[0]


def insert_genre(genre: list):
    if genre is None:
        return
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    for g in genre:
        res = cursor.execute(f'''
            SELECT count(1) FROM genre g WHERE g.genre = ?
        ''', (g,))

        exist = res.fetchone()[0] > 0
        if not exist:
            cursor.execute(f'''
                INSERT INTO genre(genre)
                VALUES(?)
            ''', (g,))
    connection.commit()


def insert_keyword(keyword: list):
    if keyword is None:
        return
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    for k in keyword:
        res = cursor.execute(f'''
            SELECT count(1) FROM keyword g WHERE g.word = ?
        ''', (k,))

        exist = res.fetchone()[0] > 0
        if not exist:
            cursor.execute(f'''
                INSERT INTO keyword(word)
                VALUES(?)
            ''', (k,))
    connection.commit()


def insert_director(director):
    if director is None:
        return
    insert_actor([director])


def insert_actor(actor: list):
    if actor is None:
        return
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    for a in actor:
        res = cursor.execute(f'''
            SELECT count(1) FROM people p WHERE p.name = ?
        ''', (a,))

        exist = res.fetchone()[0] > 0
        if not exist:
            cursor.execute(f'''
                INSERT INTO people(name)
                VALUES(?)
            ''', (a,))
    connection.commit()


def insert_is_genre(genre, movie_id):
    if genre is None:
        return
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    for g in genre:
        genre_id = get_genre_id(g)
        cursor.execute(f'''
            INSERT INTO is_genre(genre_id, movie_id)
            VALUES(?, ?)
        ''', (genre_id, movie_id))
    connection.commit()


def insert_act_in(actor: list, movie_id):
    if actor is None:
        return
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    for a in actor:
        cursor.execute(f'''
            INSERT INTO act_in(movie_id, actor_id)
            VALUES(?, ?)
        ''', (get_director_or_actor_id(a), movie_id,))
    connection.commit()

def insert_has_keyword(keyword: list, movie_id):
    if keyword is None:
        return
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    for a in keyword:
        cursor.execute(f'''
            INSERT INTO has_keyword(keyword_id, movie_id)
            VALUES(?, ?)
        ''', (get_keyword_id(a), movie_id,))
    connection.commit()


def imdb_insert_movie(**kwargs):
    def validate_img_link(link):
        if requests.head(link).status_code != HTTPStatus.OK:
            return None
        return link
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    cursor.execute(f'''
                INSERT INTO movie(id, title, poster_link, year, imdb_rating, runtime, overview, director_id)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            ''', (kwargs['movie_id'], kwargs['title'], validate_img_link(kwargs['poster_link']),
                  kwargs['year'], kwargs['rating'], kwargs['runtime'], kwargs['overview'],
                  get_director_or_actor_id(kwargs['director'])))
    connection.commit()


def tmdb_insert_movie(**kwargs):
    connection = db_connection.get_connection()
    cursor = connection.cursor()
    director_id = get_director_or_actor_id(kwargs['director'])
    movie_id = get_movie_id({
        'title': kwargs['title'],
        'year': kwargs['year'],
        'director_id': director_id
    })

    if movie_id == -1:
        cursor.execute(f'''
            INSERT INTO movie(id, title, year, tmdb_rating, runtime, overview, director_id,
                tagline, homepage, budget, revenue)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            kwargs['movie_id'], kwargs['title'], kwargs['year'], kwargs['tmdb_rating'],
            kwargs['runtime'], kwargs['overview'], director_id, kwargs['tagline'],
            kwargs['homepage'], kwargs['budget'], kwargs['revenue']
        ))
    else:
        cursor.execute(f'''
            UPDATE movie
            SET tmdb_rating = ?, tagline = ?, homepage = ?, budget = ?, revenue = ?
            WHERE id = ?
        ''', (
            kwargs['tmdb_rating'], kwargs['tagline'], kwargs['homepage'], kwargs['budget'], kwargs['revenue'],
            movie_id
        ))

    connection.commit()


def import_imdb_dataset(base=0):
    imdb_df = pd.read_csv("./imdb_top_1000.csv")
    cnt = base
    for index, row in imdb_df.iterrows():
        movie_id = index + base
        poster_link = row['Poster_Link']
        series_title = row['Series_Title']
        release_year = row['Released_Year']
        runtime = row['Runtime']
        genre = row['Genre'].split(', ')
        imdb_rating = row['IMDB_Rating']
        overview = row['Overview']
        director = row['Director']
        star = [row['Star1'], row['Star2'], row['Star3'], row['Star4']]

        insert_genre(genre)
        insert_director(director)
        insert_actor(star)
        imdb_insert_movie(movie_id=movie_id, title=series_title, poster_link=poster_link,
                          year=release_year, rating=imdb_rating, runtime=runtime, overview=overview,
                          director=director)
        insert_is_genre(genre, movie_id)
        insert_act_in(star, movie_id)
        cnt += 1
        print(f'''inserted {cnt} movies''')
    return cnt


def import_tmdb_dataset(base=0):
    def valid(s):
        return s is not None and isinstance(s, str)
    tmdb_df = pd.read_csv('./tmdb_movies_data.csv')
    cnt = base
    for index, row in tmdb_df.iterrows():
        movie_id = base + index
        tmdb_rating = row['vote_average']
        release_year = row['release_year']
        genre = row['genres'].split('|') if valid(row['genres']) else None
        overview = row['overview']
        keyword = str(row['keywords']).split('|') if valid(row['keywords']) else None
        tagline = row['tagline']
        director = row['director']
        homepage = row['homepage']
        cast = row['cast'].split('|') if valid(row['cast'])else None
        title = row['original_title']
        budget = row['budget']
        revenue = row['revenue']
        runtime = str(row['runtime']) + ' min'

        insert_genre(genre)
        insert_keyword(keyword)
        insert_director(director)
        insert_actor(cast)
        tmdb_insert_movie(movie_id=movie_id, title=title, year=release_year, tmdb_rating=tmdb_rating,
                          overview=overview, tagline=tagline, homepage=homepage, budget=budget,
                          revenue=revenue, runtime=runtime, director=director)
        insert_is_genre(genre, movie_id)
        insert_act_in(cast, movie_id)
        insert_has_keyword(keyword, movie_id)
        cnt += 1
        print(f'''inserted {cnt} movies''')
    return cnt

def delete_all():
    connection = db_connection.get_connection()
    cursor = connection.cursor()

    cursor.execute(f'''
        DELETE FROM genre
    ''')
    cursor.execute(f'''
            DELETE FROM people
        ''')
    cursor.execute(f'''
            DELETE FROM keyword
        ''')
    cursor.execute(f'''
            DELETE FROM movie
        ''')
    cursor.execute(f'''
            DELETE FROM has_keyword
        ''')
    cursor.execute(f'''
            DELETE FROM is_genre
        ''')
    cursor.execute(f'''
            DELETE FROM user
        ''')
    cursor.execute(f'''
            DELETE FROM like_movie
        ''')

def main():
    build_schema()
    cnt = import_imdb_dataset()
    import_tmdb_dataset(cnt)


if __name__ == '__main__':
    main()
