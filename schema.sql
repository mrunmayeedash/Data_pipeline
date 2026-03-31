-- Create database
CREATE DATABASE IF NOT EXISTS moviedb;
USE moviedb;

-- =========================
-- MOVIES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255),
    release_year INT,
    director VARCHAR(255),
    plot TEXT,
    box_office VARCHAR(50)
);

-- =========================
-- GENRES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(100) UNIQUE
);

-- =========================
-- MOVIE_GENRES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

-- =========================
-- RATINGS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    user_id INT,
    rating FLOAT,
    rating_timestamp DATETIME,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);
