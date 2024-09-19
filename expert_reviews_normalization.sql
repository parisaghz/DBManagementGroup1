--author: Ghazaleh

alter table expert_reviews 
add column expert_id int


update expert_reviews 
set expert_id = (select expert_profile.id
from expert_profile where expert_reviews.expert_name = expert_profile.user_name)

select * from expert_reviews

select * from expert_profile



alter table expert_reviews 
drop column expert_name 


alter table expert_reviews
add constraint fk_expert_profile 

foreign key (expert_id)
references expert_profile (id)


select * from expert_reviews
