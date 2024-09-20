---normalization of movie_info and user_reviews by removing url and adding the movie_id as the foreign key into the user_reviews table
--- Arezoo Amani/ student ID: 500948377
alter table user_reviews
add column movie_id bigint

update user_reviews ur
set movie_id = mi.id
from movie_info mi
where ur.url = mi.url

alter table user_reviews
add constraint fk_movie_info
foreign key (movie_id) references movie_info(id)

select ui.*, mi.movie_title
from user_reviews ui
join movie_info mi on ui.movie_id = mi.id

alter table user_reviews
drop column url

select * from user_reviews
