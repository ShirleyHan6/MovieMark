CREATE TABLE genre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT
);

CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE keyword (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT
);

CREATE TABLE movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    poster_link TEXT,
    year INTEGER,
    imdb_rating FLOAT,
    tmdb_rating FLOAT,
    runtime TEXT,
    overview TEXT,
    director_id INTEGER,
    tagline TEXT,
    homepage TEXT,
    budget INTEGER,
    revenue INTEGER,
    FOREIGN KEY (director_id) REFERENCES people(id)
);

CREATE TABLE has_keyword (
    movie_id INTEGER,
    keyword_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movie(id),
    FOREIGN KEY(keyword_id) REFERENCES keyword(id)
);


CREATE TABLE act_in (
    movie_id INTEGER,
    actor_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movie(id),
    FOREIGN KEY(actor_id) REFERENCES people(id)
);

CREATE TABLE is_genre (
    movie_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movie(id),
    FOREIGN KEY(genre_id) REFERENCES genre(id)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);

CREATE TABLE like_movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    watched INTEGER,
    timestamp DATE,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE TABLE review (
    user_id INTEGER,
    movie_id INTEGER,
    timestamp DATE,
    content TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (movie_id) REFERENCES movie(id)
);