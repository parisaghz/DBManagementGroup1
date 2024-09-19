-- Hypothese based on article 3:
-- “Negative reviews have a stronger negative impact on box office performance
-- for literary genres like Romance and Drama compared to action or adventure films.”


WITH expert_rating AS (
    SELECT 
        er.movie_id,
        AVG(CAST(er.individual_score AS NUMERIC)) AS avg_expert_score 
    FROM 
        expert_reviews er 
    WHERE 
        er.individual_score IS NOT NULL 
        AND er.individual_score <> '' 
        AND er.individual_score !~ '[^0-9.]' 
    GROUP BY 
        er.movie_id),

genre_info AS (
    SELECT 
        mg.movie_id,
        mg.genre_id
    FROM 
        movie_genres mg
		where mg.genre_id in(4,17)
)

SELECT 
    mi.movie_title, 
	mi.release_date,
	release_year,
    mi.opening_weekend, 
    genre_info.genre_id, 
    expert_rating.avg_expert_score
FROM 
    movie_info mi
JOIN 
    expert_rating ON mi.id = expert_rating.movie_id

JOIN 
    genre_info ON mi.id = genre_info.movie_id
ORDER BY 
    mi.opening_weekend DESC;