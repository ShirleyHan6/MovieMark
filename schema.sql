CREATE TABLE genre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT
);

CREATE INDEX genre_index ON genre(genre);

CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE INDEX people_index ON people(name);

CREATE TABLE keyword (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT
);

CREATE INDEX keyword_index ON keyword(word);

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

CREATE INDEX movie_index ON movie(title, year, director_id);

CREATE TABLE has_keyword (
    movie_id INTEGER,
    keyword_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movie(id),
    FOREIGN KEY(keyword_id) REFERENCES keyword(id)
);

CREATE INDEX has_keyword_index ON has_keyword(movie_id, keyword_id);

CREATE TABLE act_in (
    movie_id INTEGER,
    actor_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movie(id),
    FOREIGN KEY(actor_id) REFERENCES people(id)
);

CREATE INDEX act_in_index ON act_in(movie_id, actor_id);

CREATE TABLE is_genre (
    movie_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movie(id),
    FOREIGN KEY(genre_id) REFERENCES genre(id)
);

CREATE INDEX is_genre_index ON is_genre(movie_id, genre_id);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);

CREATE INDEX user_index ON user(username);

CREATE TABLE like_movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    watched INTEGER,
    save_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE INDEX like_movie_index ON like_movie(user_id, movie_id);

CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    content TEXT,
    post_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE INDEX review_index ON review(user_id, movie_id);