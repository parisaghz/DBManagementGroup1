import csv
from config import load_config
import psycopg2

def write_results_to_csv():
    config = load_config()
    query = """
    WITH expert_rating AS (
        SELECT 
            er.movie_id,
            AVG(CAST(er.individual_score AS NUMERIC)) AS avg_expert_score 
        FROM 
            expert_reviews er 
        WHERE 
            er.individual_score IS NOT NULL 
            AND er.individual_score <> '' 
            AND er.individual_score !~ '[^0-9.]' 
        GROUP BY 
            er.movie_id
    ),

    genre_info AS (
        SELECT 
            mg.movie_id,
            mg.genre_id
        FROM 
            movie_genres mg
        WHERE 
            mg.genre_id IN (4, 17)
    )

    SELECT 
        mi.movie_title, 
        mi.release_date,
        mi.release_year,  -- Ensure this is correctly referenced from the movie_info table
        mi.opening_weekend, 
        genre_info.genre_id, 
        expert_rating.avg_expert_score
    FROM 
        movie_info mi
    JOIN 
        expert_rating ON mi.id = expert_rating.movie_id
    JOIN 
        genre_info ON mi.id = genre_info.movie_id
    ORDER BY 
        mi.opening_weekend DESC;
    """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

                with open('result5th.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Movie Title', 'Release Date', 'Release Year', 'Opening Weekend', 'Genre ID', 'Avg Expert Score'])  # Updated header
                    for row in rows:
                        writer.writerow(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    write_results_to_csv()