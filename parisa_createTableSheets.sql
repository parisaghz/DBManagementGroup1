--author : Parisa Ghazanfari 500955367

--create sales
create table sales( 
id SERIAL PRIMARY KEY,
year text,
release_date text,
title text,
genre text,
international_box_office text,
domestic_box_office text,
worldwide_box_office text,
production_budget text,
opening_weekend text,
url text
)

--create meta
create table meta(
id SERIAL PRIMARY KEY,
url text,
title text,
run_time text,
director text,
genre text,
meta_score text,
user_score text
)

--create user_review_source
create table user_review_source(
id SERIAL PRIMARY KEY,
url text,
individual_score text,
reviewer_name text,
post_date text,
review_text text,
thumbs_up text,
tumbs_total text,
word_count text,
tone text,
negate text,
negative_emotion text,
positive_emotion text
)

--create expert_review_source
create table expert_review_source(
id SERIAL PRIMARY KEY,
url text,
individual_score text,
reviewer_name text,
post_date text,
review_text text,
word_count text,
tone text,
negate text,
positive_emotion text,
negative_emotion text
)
