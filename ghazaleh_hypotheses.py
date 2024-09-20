import csv
from config import load_config
import psycopg2

def write_results_to_csv():
    config = load_config()
    query = """
    WITH expert_rating AS (
        SELECT er.movie_id,
               AVG(CAST(er.individual_score AS NUMERIC)) AS avg_expert_score
        FROM expert_reviews er
        WHERE er.individual_score IS NOT NULL 
          AND er.individual_score <> '' 
          AND er.individual_score !~ '[^0-9.]'  -- Exclude any non-numeric characters
        GROUP BY er.movie_id
    ),

    user_rating AS (
        SELECT ur.movie_id,
               AVG(CAST(ur.individual_score AS NUMERIC)) AS avg_user_score
        FROM user_reviews ur
        WHERE ur.individual_score IS NOT NULL 
          AND ur.individual_score <> '' 
          AND ur.individual_score !~ '[^0-9.]'  -- Exclude any non-numeric characters
        GROUP BY ur.movie_id
    )

    SELECT mi.movie_title, mi.opening_weekend, 
           expert_rating.avg_expert_score, user_rating.avg_user_score
    FROM movie_info mi
    JOIN expert_rating ON mi.id = expert_rating.movie_id
    JOIN user_rating ON mi.id = user_rating.movie_id
    ORDER BY mi.opening_weekend DESC
    """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

                with open('results1.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Movie Title', 'Opening Weekend', 'Avg Expert Score', 'Avg User Score'])
                    for row in rows:
                        writer.writerow(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    write_results_to_csv()
