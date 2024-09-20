import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV into a DataFrame
df = pd.read_csv('results1.csv')

# Convert 'Opening Weekend' to a numeric type if it's not already
df['Opening Weekend'] = pd.to_numeric(df['Opening Weekend'], errors='coerce')

# Set the style of seaborn plot
sns.set(style="whitegrid")

# Create a line plot for both 'Avg Expert Score' and 'Avg User Score' against 'Opening Weekend'
plt.figure(figsize=(10,6))

# Plot for Expert Score
sns.lineplot(x='Opening Weekend', y='Avg Expert Score', data=df, label='Avg Expert Score', marker="o")

# Plot for User Score
sns.lineplot(x='Opening Weekend', y='Avg User Score', data=df, label='Avg User Score', marker="o")

# Add labels and title
plt.xlabel('Opening Weekend Revenue')
plt.ylabel('Average Scores')
plt.title('Opening Weekend Revenue vs Average Expert/User Scores')
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
