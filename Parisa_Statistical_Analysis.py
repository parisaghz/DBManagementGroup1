import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_results():
    # load the CSV file into a DataFrame
    df = pd.read_csv('results.csv')

    # adjust the y-axis to show box office in billions
    df['Avg Box Office'] = df['Avg Box Office'] / 1e9

    # scatter plot with regression line
    plt.figure(figsize=(10, 6))

    sns.scatterplot(x='Avg Emotional Tone', y='Avg Box Office', data=df, hue='Genre Name', s=100)

    # add regression line to compare results
    sns.regplot(x='Avg Emotional Tone', y='Avg Box Office', data=df, scatter=False, color='gray', line_kws={"linewidth":2})

    # design the plot
    plt.title('Average Emotional Tone vs. Average Box Office by Genre', fontsize=16)
    plt.xlabel('Avg Emotional Tone', fontsize=12)
    plt.ylabel('Avg Box Office (in billions)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend placement
    plt.tight_layout()  # Ensure everything fits

    plt.show()

if __name__ == '__main__':
    visualize_results()
