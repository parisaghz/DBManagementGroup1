--author: ghazaleh
--create expert_reviews


create table expert_profile(  ---at fist we create expert profile table to have a id and name for each reviewer--- 
id serial primary key,
user_name varchar(255)
)

insert into expert_profile (user_name)   --- we get the data from the source that is the cleaned table from the excel sheet--- 
select distinct reviewer_name 
from expert_review_source

select * from expert_profile