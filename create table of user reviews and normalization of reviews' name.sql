--- create table for the name of reviewer and set an id for them in order to use their id as the foreign keys in user_reviews table to avoid repetion of reviewers' name.
--- Auther: Arezoo Amani/ student ID: 500948377

create table user_profile(
user_id serial primary key,
user_name varchar(255) unique
)

insert into user_profile(user_name)
select distinct reviewer_name
from user_review_source

select * from user_profile

create table user_reviews(
id serial primary key,
user_name varchar(255),
individual_score text,
review_date varchar(20),
review_text text,
thumbs_up text,
thumbs_total text,
word_count varchar(30),
tone varchar(30),
positive_emotion varchar(50),
negative_emotion varchar(50),
url text
)

insert into user_reviews(user_name, individual_score, review_date, review_text, thumbs_up, thumbs_total, word_count, tone, positive_emotion, negative_emotion, url)
select reviewer_name, individual_score, post_date, review_text, thumbs_up, thumbs_total, word_count, tone, positive_emotion, negative_emotion, url
from user_review_source


---add the column of user_id to the user_review table as the foreign key and removie the column of user_name from the user_reviews table

alter table user_reviews
add column user_id int

update user_reviews
set user_id = (select u.user_id from user_profile u where user_reviews.user_name = u.user_name)

select * from user_reviews
select * from user_profile

alter table user_reviews
drop column user_name

alter table user_reviews
add constraint fk_user_profile
foreign key (user_id) references user_profile(user_id)
