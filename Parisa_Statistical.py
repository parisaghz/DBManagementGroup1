# Author: Parisa Ghazanfari 500955367

import csv
import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Parisa_Database_Config import load_config

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
        WHERE gt.id IN (2, 9, 10, 17)  -- Genres you are focusing on
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

                # Write the results to a CSV
                with open('results2.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Genre Name', 'Avg Emotional Tone', 'Avg Box Office'])
                    for row in rows:
                        writer.writerow(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def visualize_results():
    """ Load the results and create a scatter plot with a comparison line """
    # Load the CSV file into a DataFrame
    df = pd.read_csv('results2.csv')

    # Adjust the y-axis to show box office in billions
    df['Avg Box Office'] = df['Avg Box Office'] / 1e9

    # Scatter plot with regression line
    plt.figure(figsize=(10, 6))

    # Plot scatter plot with hue for genres
    sns.scatterplot(x='Avg Emotional Tone', y='Avg Box Office', data=df, hue='Genre Name', s=100)

    # Add regression line to compare results
    sns.regplot(x='Avg Emotional Tone', y='Avg Box Office', data=df, scatter=False, color='gray', line_kws={"linewidth":2})

    # Customize the plot
    plt.title('Average Emotional Tone vs. Average Box Office by Genre (Selected)', fontsize=16)
    plt.xlabel('Avg Emotional Tone', fontsize=12)
    plt.ylabel('Avg Box Office (in billions)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend placement
    plt.tight_layout()  # Ensure everything fits

    # Show the plot
    plt.show()

if __name__ == '__main__':
    write_results_to_csv()
    visualize_results()
