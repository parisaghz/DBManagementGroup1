#author : Parisa Ghazanfari 500955367

import csv
import psycopg2
from config import load_config

def write_results_to_csv():
    """ Execute the query and write results to a CSV file """
    config = load_config()
    query = """
    WITH genreReview AS (
        SELECT gt.genre_name, mg.movie_id,
        AVG(CAST(ur.tone AS NUMERIC)) AS avg_emotional_tone,
        mi.worldwide_box_office
        FROM genre_types gt
        JOIN movie_genres mg ON gt.id = mg.genre_id
        JOIN user_reviews ur ON mg.movie_id = ur.movie_id
        JOIN movie_info mi ON mi.id = ur.movie_id
        WHERE gt.id IN (2, 9, 10, 17)
        GROUP BY gt.genre_name, mg.movie_id, mi.worldwide_box_office
    ),
    genreComparison AS (
        SELECT genre_name,
        AVG(avg_emotional_tone) AS avg_genre_emotional_tone,
        AVG(CAST(worldwide_box_office AS NUMERIC)) AS avg_genre_box_office
        FROM genreReview 
        GROUP BY genre_name
    )
    SELECT genre_name, avg_genre_emotional_tone, avg_genre_box_office
    FROM genreComparison
    ORDER BY avg_genre_box_office DESC;
    """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

                with open('results2.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Genre Name', 'Avg Emotional Tone', 'Avg Box Office'])
                    for row in rows:
                        writer.writerow(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    write_results_to_csv()
