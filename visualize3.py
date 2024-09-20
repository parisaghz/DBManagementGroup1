import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Julian_database_config import load_config
import psycopg2

def write_results_to_csv():
    config = load_config()
    query = """
    SELECT 
        mi.movie_title, 
        mi.worldwide_box_office,
        mi.international_box_office,
        mi.domestic_box_office,
        COUNT(er.id) AS total_expert_reviews, 
        AVG(CASE 
                WHEN er.individual_score ~ '^[0-9.]+$' THEN CAST(er.individual_score AS numeric) 
                ELSE NULL 
            END) AS avg_expert_score,
        AVG(CASE 
                WHEN er.positive_emotion ~ '^[0-9.]+$' THEN CAST(er.positive_emotion AS numeric) 
                ELSE NULL 
            END) AS avg_positive_emotion,
        AVG(CASE 
                WHEN er.tone ~ '^[0-9.]+$' THEN CAST(er.tone AS numeric) 
                ELSE NULL 
            END) AS avg_tone
    FROM 
        movie_info mi
    JOIN 
        expert_reviews er ON mi.id = er.movie_id
    GROUP BY 
        mi.id
    ORDER BY 
        total_expert_reviews DESC;
    """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

                # Write the results to a CSV file
                with open('results_with_tone_and_emotion.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Movie Title', 'Worldwide Box Office', 'International Box Office', 
                                     'Domestic Box Office', 'Total Expert Reviews', 'Avg Expert Score', 
                                     'Avg Positive Emotion', 'Avg Tone'])
                    for row in rows:
                        writer.writerow(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

# Visualize the data using seaborn
def visualize_data():
    # Load the data from the CSV file into a DataFrame
    df = pd.read_csv('results_with_tone_and_emotion.csv')

    # Convert the box office columns to numeric, removing any non-numeric characters
    df['Worldwide Box Office'] = pd.to_numeric(df['Worldwide Box Office'], errors='coerce')
    df['International Box Office'] = pd.to_numeric(df['International Box Office'], errors='coerce')
    df['Domestic Box Office'] = pd.to_numeric(df['Domestic Box Office'], errors='coerce')

    # Create subplots: one for positive emotion and one for tone
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Positive Emotion
    scatter1 = axes[0].scatter(df['Avg Expert Score'], df['Worldwide Box Office'], 
                               c=df['Avg Positive Emotion'], cmap='coolwarm', 
                               alpha=0.7, edgecolors="w", linewidth=1)
    sns.regplot(x='Avg Expert Score', y='Worldwide Box Office', data=df, scatter=False, color="red", ax=axes[0])
    cbar1 = fig.colorbar(scatter1, ax=axes[0])
    cbar1.set_label('Avg Positive Emotion')
    axes[0].set_title('Expert Score vs Worldwide Box Office\n(Color = Positive Emotion)')
    axes[0].set_xlabel('Average Expert Score')
    axes[0].set_ylabel('Worldwide Box Office')

    # Subplot 2: Tone
    scatter2 = axes[1].scatter(df['Avg Expert Score'], df['Worldwide Box Office'], 
                               c=df['Avg Tone'], cmap='viridis', 
                               alpha=0.7, edgecolors="w", linewidth=1)
    sns.regplot(x='Avg Expert Score', y='Worldwide Box Office', data=df, scatter=False, color="red", ax=axes[1])
    cbar2 = fig.colorbar(scatter2, ax=axes[1])
    cbar2.set_label('Avg Tone')
    axes[1].set_title('Expert Score vs Worldwide Box Office\n(Color = Tone)')
    axes[1].set_xlabel('Average Expert Score')
    axes[1].set_ylabel('Worldwide Box Office')

    # Show the plot
    plt.tight_layout()
    plt.show()

# Run the script
if __name__ == '__main__':
    write_results_to_csv()  # Fetch data and write to CSV
    visualize_data()        # Create enhanced visualization