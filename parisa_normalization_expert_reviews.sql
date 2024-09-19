--author : Parisa Ghazanfari 500955367
--normalization for expert_reviews and set foreign key (novie_id)
alter table expert_reviews
add column movie_id bigint

update expert_reviews er
set movie_id = mi.id
from movie_info mi
where er.url = mi.url


alter table expert_reviews
add constraint fk_movie_info
foreign key (movie_id) references movie_info(id)


select ei.*, mi.movie_title
from expert_reviews ei
join movie_info mi on ei.movie_id = mi.id


alter table expert_reviews
drop column url

