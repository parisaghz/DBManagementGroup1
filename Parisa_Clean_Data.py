#author : Parisa Ghazanfari 500955367

import pandas as pd      #for reading , writing data
import re                #to clean data

# reading csv file
data = pd.read_csv('/Users/parisa/Desktop/sales.csv')

#remove character that is not a-z and A-Z or 0-9
def remove_unwanted_chars(input_string):
 return re.sub(r'[^a-zA-Z0-9]', '', input_string)

#start to clean data for specified columns
# astype(str) for ensuring that values are strings
data['Rev'] = data['Rev'].astype(str).apply(remove_unwanted_chars)

#save the new csv file
data.to_csv('/Users/parisa/Desktop/UserReviewsClean.csv', index=False)

#print for users
print("Cleaned data saved to metasales.csv")