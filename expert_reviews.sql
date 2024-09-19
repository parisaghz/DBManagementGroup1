--author: Ghazaleh

create table expert_reviews(   --- in the second step we create the expert reviews table and we have to add all the data related to expert review---
id serial primary key,
individual_score text,
expert_name varchar(255),
url text,
review_date varchar(20),
positive_emotion varchar(50),
negative_emotion varchar(50),
wordcount varchar(30),
review_text text,
tone varchar(30)
)


insert into expert_reviews (individual_score,  ----again we get the data from the excel sheet which we cleaned them --- 
expert_name,
url,
review_date,
positive_emotion,
negative_emotion,
wordcount,
review_text,
tone)
select individual_score,
reviewer_name,
url,
post_date,
positive_emotion,
negative_emotion,
word_count,
review_text,
tone
from expert_review_source 
