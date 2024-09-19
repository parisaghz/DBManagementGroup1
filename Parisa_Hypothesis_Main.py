import csv                            #for writing data in csv format
from config import load_config        #function to load db configuration
import psycopg2                       #connecting python with postgres

# function to execute query and write in csv
def write_results_to_csv():
    config = load_config()
    # sql query
    query = """
    WITH genreReview AS (
        SELECT gt.genre_name, mg.movie_id,
        AVG(CAST(ur.tone AS NUMERIC)) AS avg_emotional_tone,
        mi.worldwide_box_office
        FROM genre_types gt
        JOIN movie_genres mg ON gt.id = mg.genre_id
        JOIN user_reviews ur ON mg.movie_id = ur.movie_id
        JOIN movie_info mi ON mi.id = ur.movie_id
        WHERE gt.id BETWEEN 1 AND 24 AND gt.id <> 11
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
            with conn.cursor() as cur:         #create new cursor
                cur.execute(query)             #execure query
                rows = cur.fetchall()          #fetch all the rows

                with open('results1.csv', 'w', newline='') as file:                           #writing query results to csv file
                    writer = csv.writer(file)
                    writer.writerow(['Genre Name', 'Avg Emotional Tone', 'Avg Box Office'])   # writes the header row 
                    for row in rows:
                        writer.writerow(row)

    except (Exception, psycopg2.DatabaseError) as error:              #handling exception
        print(error)

#if script run as main program
if __name__ == '__main__':
    write_results_to_csv()
