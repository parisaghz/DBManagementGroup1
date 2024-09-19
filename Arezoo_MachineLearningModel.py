import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


conn = psycopg2.connect(host = "localhost", database = "postgres", user = "postgres", password = "****", port = 5433)
cur = conn.cursor()

##define the sql query and set the result into the pandas dataframe in order to clean the data and work on them 

sql_query = """select 
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

cur.execute(sql_query)
columns = ["movie_id", "movie_title", "production_budget", "worldwide_box_office", "avg_user_negative_emotion", "avg_expert_negative_emotion"]
data = cur.fetchall()
df = pd.DataFrame(data, columns = columns)

cur.close()
conn.close()

#print(df)

##All the data are 6587 rows 
##Cleaning the data and remove the rows that inculdes null values
##After cleaning only 2522 rows remain
df.dropna(inplace=True)
print(df)

##Set the data for x and y, attributes that assigned to X are independent features in our model 
##and attribute in y is the dependent variable that by manipulating the independent variable will change.
X = df[["production_budget", "avg_user_negative_emotion", "avg_expert_negative_emotion"]]
y = df["worldwide_box_office"]

##split data in two parts, %80 for training the model %20 for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

##train the linear regression model
box_office_model = LinearRegression().fit(X_train, y_train)

##calculate the predicted value for test data by our model
y_prediction = box_office_model.predict(X_test)

##Evaluate the model by calculating the mean squared error and r2 score
mse = mean_squared_error(y_test, y_prediction)
r2 = r2_score(y_test, y_prediction)


print(f"Mean square error: {round(mse, 5)}")
print(f"R-squared: {round(r2, 5)}")

##Plot actual data and predicted values
##The model doesn't predict accurately because we have to add more features to examine accurately how box
## office will affect by the features such as negative emotions, production budget, tone, individual score etc. 
plt.scatter(y_test, y_prediction, alpha=0.5)
plt.plot([min(y_test), max(y_test)], [min(y_prediction), max(y_prediction)], color = "purple", linestyle = "--")
plt.xlabel("Real box office")
plt.ylabel("Predicted box office")
plt.title("Read vs Predicted Box Office")
plt.show()