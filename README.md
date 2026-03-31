# Project Description: Movie Data Engineering Pipeline

Designed and implemented an end-to-end Movie Data Engineering Pipeline using Python and MySQL to ingest, enrich, transform, and analyze movie data. The pipeline extracts movie and rating data from the MovieLens dataset (CSV files) and enriches it with additional metadata such as director, plot, and box office information using the OMDb REST API. Data cleaning and transformation were performed using pandas, including handling missing values, extracting release years, and normalizing genre information into relational tables.

The transformed data was loaded into a MySQL relational database using PyMySQL, with a well-structured schema consisting of movies, genres, movie-genre mappings, and ratings tables. Foreign key constraints were used to maintain data integrity, and idempotent inserts (INSERT IGNORE) ensured safe re-execution of the ETL pipeline without duplication. Analytical SQL queries were written to derive insights such as highest-rated movies, top-rated genres, most prolific directors, and year-wise average ratings.

This project demonstrates practical experience in ETL pipeline development, API integration, relational data modeling, and SQL-based analytics, closely simulating real-world data engineering workflows.
