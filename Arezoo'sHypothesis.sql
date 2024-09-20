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

---test the result to see how it works. First categorise the movies into two groups based their production budget
---Then calculate the average of negative emotion for expert and user reviews, and check to see if the impact of negative emotion
--- on the movies with high budget is less than movies with low budget
	
with median_budget as(
select percentile_cont(0.5) within group (order by cast(production_budget as numeric)) as median_production_budget
from movie_info
),
categorized_movies as (
select 
	mi.id, 
	mi.movie_title,
	mi.production_budget,
	mi.worldwide_box_office,
	avg(cast(ur.negative_emotion as numeric)) as avg_user_negative_emotion,
	avg(cast(er.negative_emotion as numeric)) as avg_expert_negative_emotion,
	case
		when cast(mi.production_budget as numeric) >= (select median_production_budget from median_budget)
		then 'High budget'
		else 'Low budget'
	end as budget_category
from movie_info mi
join user_reviews ur on mi.id = ur.movie_id
join expert_reviews er on mi.id = er.movie_id
group by mi.id, mi.movie_title, mi.production_budget, mi.worldwide_box_office
)
select 
	budget_category,
	avg(cast(production_budget as numeric)) as avg_production_budget,
    avg(cast(worldwide_box_office as numeric)) as avg_worldwide_box_office,
    avg(cast(avg_user_negative_emotion as numeric)) as avg_user_negative_emotion,
    avg(cast(avg_expert_negative_emotion as numeric)) as avg_expert_negative_emotion
from categorized_movies
group by budget_category

---------------------------------

---Check the avwrage of of tone, negative emotion and production budget in reviews for the future use

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


