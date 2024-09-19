-- Movies with higher user and expert review ratings will have a stronger opening weekend box office 
-- performance.

with expert_rating as (
select er.movie_id,
AVG (cast (er.individual_score as NUMERIC)) as avg_expert_score 
from expert_reviews er 
where 
er.individual_score IS NOT NULL 
AND er.individual_score <> '' 
AND er.individual_score !~ '[^0-9.]'  
group by er.movie_id
),

user_rating as (
select ur.movie_id,
AVG (cast (ur.individual_score as NUMERIC)) as avg_user_score
from user_reviews ur
where 
ur.individual_score IS NOT NULL 
AND ur.individual_score <> '' 
AND ur.individual_score !~ '[^0-9.]' 
group by ur.movie_id
)

select mi.movie_title, mi.opening_weekend, expert_rating.avg_expert_score, user_rating.avg_user_score 
from movie_info mi

join expert_rating on mi.id = expert_rating.movie_id
join user_rating on mi.id = user_rating.movie_id 


order by mi.opening_weekend desc
