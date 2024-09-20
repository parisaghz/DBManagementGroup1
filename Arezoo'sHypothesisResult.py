#Arezoo

import csv
from ArezooConfig import load_config
import psycopg2

def write_result_to_csv():
    config = load_config()
        query = """with median_budget as(
        select percentile_cont(0.5) within group (order by cast(production_budget as numeric)) as median_production_budget
        from movie_info
        ),
        categorized_movies as (
        select 
            mi.id, 
            mi.movie_title,
            mi.production_budget,
            mi.worldwide_box_office,
            avg(cast(ur.negative_emotion as numeric)) as avg_user_negative_emotion,
            avg(cast(er.negative_emotion as numeric)) as avg_expert_negative_emotion,
            case
                when cast(mi.production_budget as numeric) >= (select median_production_budget from median_budget)
                then 'High budget'
                else 'Low budget'
            end as budget_category
        from movie_info mi
        join user_reviews ur on mi.id = ur.movie_id
        join expert_reviews er on mi.id = er.movie_id
        group by mi.id, mi.movie_title, mi.production_budget, mi.worldwide_box_office
        )
        select 
            budget_category,
            avg(cast(production_budget as numeric)) as avg_production_budget,
            avg(cast(worldwide_box_office as numeric)) as avg_worldwide_box_office,
            avg(cast(avg_user_negative_emotion as numeric)) as avg_user_negative_emotion,
            avg(cast(avg_expert_negative_emotion as numeric)) as avg_expert_negative_emotion
        from categorized_movies
        group by budget_category"""

    try:
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            print(f"Fetched {len(rows)} rows.")  # Print the number of rows fetched

            if not rows:
                print("No data retrieved from the query.")
                return  # Exit if no data is available

            with open('/Users/arezoo/Documents/Python/projects/result2.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["budget_category", "avg_production_budget", "avg_worldwide_box_office", "avg_user_negative_emotion", "avg_expert_negative_emotion"])
                for row in rows:
                    writer.writerow(row)
                print("CSV file created successfully.")  # Confirm CSV creation

    except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error: {error}")


if __name__ == '__main__':
    write_result_to_csv()


