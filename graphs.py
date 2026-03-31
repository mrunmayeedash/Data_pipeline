import pymysql
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# DATABASE CONFIG
# =========================
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456789",   # change this
    database="moviedb",
    port=3306
)

print("✅ Connected to MySQL")

# =========================
# 1. Average Rating by Release Year (LINE GRAPH)
# =========================
query_year_rating = """
SELECT
    m.release_year AS year,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM movies m
JOIN ratings r
    ON m.movie_id = r.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year;
"""

df_year_rating = pd.read_sql(query_year_rating, conn)

plt.figure()
plt.plot(df_year_rating["year"], df_year_rating["avg_rating"])
plt.xlabel("Release Year")
plt.ylabel("Average Rating")
plt.title("Average Movie Rating by Release Year")
plt.show()

# =========================
# 2. Top 10 Movies by Average Rating (BAR GRAPH)
# =========================
query_top_movies = """
SELECT
    m.title,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM movies m
JOIN ratings r
    ON m.movie_id = r.movie_id
GROUP BY m.movie_id, m.title
HAVING COUNT(r.rating) >= 50
ORDER BY avg_rating DESC
LIMIT 10;
"""

df_top_movies = pd.read_sql(query_top_movies, conn)

plt.figure()
plt.barh(df_top_movies["title"], df_top_movies["avg_rating"])
plt.xlabel("Average Rating")
plt.ylabel("Movie Title")
plt.title("Top 10 Movies by Average Rating")
plt.gca().invert_yaxis()
plt.show()

# =========================
# 3. Genre Distribution (BAR GRAPH)
# =========================
query_genre_count = """
SELECT
    g.genre_name,
    COUNT(mg.movie_id) AS movie_count
FROM genres g
JOIN movie_genres mg
    ON g.genre_id = mg.genre_id
GROUP BY g.genre_name
ORDER BY movie_count DESC;
"""

df_genre_count = pd.read_sql(query_genre_count, conn)

plt.figure()
plt.bar(df_genre_count["genre_name"], df_genre_count["movie_count"])
plt.xlabel("Genre")
plt.ylabel("Number of Movies")
plt.title("Number of Movies per Genre")
plt.xticks(rotation=45)
plt.show()

# =========================
# 4. Average Rating by Genre (BAR GRAPH)
# =========================
query_genre_rating = """
SELECT
    g.genre_name,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM genres g
JOIN movie_genres mg
    ON g.genre_id = mg.genre_id
JOIN ratings r
    ON mg.movie_id = r.movie_id
GROUP BY g.genre_name
ORDER BY avg_rating DESC;
"""

df_genre_rating = pd.read_sql(query_genre_rating, conn)

plt.figure()
plt.bar(df_genre_rating["genre_name"], df_genre_rating["avg_rating"])
plt.xlabel("Genre")
plt.ylabel("Average Rating")
plt.title("Average Rating by Genre")
plt.xticks(rotation=45)
plt.show()

# =========================
# 5. Top 10 Directors by Movie Count (BAR GRAPH)
# =========================
query_directors = """
SELECT
    director,
    COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL
  AND director <> 'N/A'
GROUP BY director
ORDER BY movie_count DESC
LIMIT 10;
"""

df_directors = pd.read_sql(query_directors, conn)

plt.figure()
plt.barh(df_directors["director"], df_directors["movie_count"])
plt.xlabel("Number of Movies")
plt.ylabel("Director")
plt.title("Top 10 Directors by Movie Count")
plt.gca().invert_yaxis()
plt.show()

# =========================
# CLOSE CONNECTION
# =========================
conn.close()
print("🎉 Graph generation completed")