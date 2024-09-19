---Movies with bigger production budgets are less affected by 
---negative reviews and will still perform well at the box office 
---even if they get bad feedback.
---
---author : Arezoo Amani 500948377

----------------------------

select 
	mi.id as movie_id, 
	mi.movie_title,
	mi.production_budget,
	mi.worldwide_box_office,
	avg(cast(ur.negative_emotion as numeric)) as avg_user_negative_emotion,
	avg(cast(er.negative_emotion as numeric)) as avg_expert_negative_emotion
from movie_info mi
left join user_reviews ur on mi.id = ur.movie_id
left join expert_reviews er on mi.id = er.movie_id
group by mi.id

---------------------------------

---Check the impact of tone, negative emotion and production budget in reviews 

select 
	mi.id, 
	mi.movie_title,
	mi.production_budget,
	mi.worldwide_box_office,
	avg(cast(ur.negative_emotion as numeric)) as avg_user_negative_emotion,
	avg(cast(er.negative_emotion as numeric)) as avg_expert_negative_emotion,
	avg(cast(ur.tone as numeric)) as avg_user_tone,
	avg(cast(er.tone as numeric)) as avg_expert_tone
from movie_info mi
left join user_reviews ur on mi.id = ur.movie_id
left join expert_reviews er on mi.id = er.movie_id
group by mi.id
having
    avg(cast(ur.tone as numeric)) < 40 or avg(cast(er.tone as numeric)) < 40;


