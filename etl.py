import pandas as pd
import pymysql
import requests
from datetime import datetime

# =========================
# DATABASE CONFIG
# =========================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "moviedb",
    "port": 3306
}

# =========================
# OMDB CONFIG
# =========================
OMDB_API_KEY = "35a9876d"
OMDB_URL = "http://www.omdbapi.com/"

# =========================
# CONNECT TO MYSQL
# =========================
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
print("✅ Connected to MySQL")

# =========================
# READ CSV FILES
# =========================
movies_df = pd.read_csv("data/movies.csv")
ratings_df = pd.read_csv("data/ratings.csv")

# =========================
# FUNCTION: OMDB API CALL
# =========================
def fetch_omdb_data(title):
    try:
        params = {
            "apikey": OMDB_API_KEY,
            "t": title
        }
        response = requests.get(OMDB_URL, params=params, timeout=5)
        data = response.json()
        if data.get("Response") == "True":
            return data
    except Exception as e:
        print("API error:", e)
    return None

# =========================
# LOAD MOVIES + GENRES
# =========================
for _, row in movies_df.iterrows():

    movie_id = int(row["movieId"])
    title = row["title"]
    genres = row["genres"]

    # Extract release year
    release_year = None
    if title[-5:-1].isdigit():
        release_year = int(title[-5:-1])

    # OMDB enrichment
    omdb = fetch_omdb_data(title)
    director = omdb.get("Director") if omdb else None
    plot = omdb.get("Plot") if omdb else None
    box_office = omdb.get("BoxOffice") if omdb else None

    # Insert movie (idempotent)
    cursor.execute("""
        INSERT IGNORE INTO movies
        (movie_id, title, release_year, director, plot, box_office)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (movie_id, title, release_year, director, plot, box_office))

    # Handle genres
    for genre in genres.split("|"):
        # Insert genre
        cursor.execute("""
            INSERT IGNORE INTO genres (genre_name)
            VALUES (%s)
        """, (genre,))

        # Get genre_id
        cursor.execute("""
            SELECT genre_id FROM genres WHERE genre_name=%s
        """, (genre,))
        genre_id = cursor.fetchone()[0]

        # Map movie-genre
        cursor.execute("""
            INSERT IGNORE INTO movie_genres (movie_id, genre_id)
            VALUES (%s, %s)
        """, (movie_id, genre_id))

# =========================
# LOAD RATINGS
# =========================
for _, row in ratings_df.iterrows():

    rating_timestamp = datetime.fromtimestamp(row["timestamp"])

    cursor.execute("""
    INSERT INTO ratings (movie_id, user_id, rating, rating_timestamp)
    SELECT %s, %s, %s, %s
    FROM movies
    WHERE movie_id = %s
""", (
    int(row["movieId"]),
    int(row["userId"]),
    float(row["rating"]),
    rating_timestamp,
    int(row["movieId"])
))

# =========================
# COMMIT & CLOSE
# =========================
conn.commit()
cursor.close()
conn.close()

print("🎉 ETL Pipeline Completed Successfully")