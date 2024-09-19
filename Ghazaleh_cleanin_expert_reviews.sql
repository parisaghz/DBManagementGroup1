import pandas as pd
import re

data = pd.read_csv('/Users/ghazaleh/Desktop)

def remove_unwanted_chars(input_string):
 return re.sub(r'[^a-zA-Z0-9]', '', input_string)

data['Rev'] = data['Rev'].astype(str).apply(remove_unwanted_chars)

data.to_csv('/Users/ghazaleh/Desktop/ExpertReviewsClean.csv', index=False)

print("Cleaned data saved to metaClean43Brightspace_edited.csv")