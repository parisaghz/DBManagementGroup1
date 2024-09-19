###uthor : Arezoo Amani 500948377

import csv
from config import load_config
import psycopg2

def write_results_to_csv():
    config = load_config()
    query = """
    select 
        mi.id, 
        mi.movie_title,
        mi.production_budget,
        mi.worldwide_box_office,
        avg(cast(ur.negative_emotion as numeric)) as avg_user_negative_emotion,
        avg(cast(er.negative_emotion as numeric)) as avg_expert_negative_emotion
    from movie_info mi
    left join user_reviews ur on mi.id = ur.movie_id
    left join expert_reviews er on mi.id = er.movie_id
    group by mi.id"""

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

                with open('results.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["movie_id", "movie_title", "production_budget", "worldwide_box_office", "avg_user_negative_emotion", "avg_expert_negative_emotion"])
                    for row in rows:
                        writer.writerow(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    write_results_to_csv()
