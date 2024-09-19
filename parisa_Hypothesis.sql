--Create a common table expression for genre review
with genreReview as (
        select gt.genre_name, mg.movie_id,
        avg(CAST(ur.tone as NUMERIC)) as avg_emotional_tone,
        mi.worldwide_box_office
        from genre_types gt
        join movie_genres mg on gt.id = mg.genre_id
        join user_reviews ur on mg.movie_id = ur.movie_id
        join movie_info mi on mi.id = ur.movie_id
        where gt.id between 1 and 24 and gt.id <> 11 --except adult genre
        group by gt.genre_name, mg.movie_id, mi.worldwide_box_office
    ),
	--Create another CTE for genre comparison
    genreComparison as (
        select genre_name,
        avg(avg_emotional_tone) as avg_genre_emotional_tone,
        avg(cast(worldwide_box_office as NUMERIC)) as avg_genre_box_office
        from genreReview 
        group by genre_name
    )
	--final query
    select genre_name, avg_genre_emotional_tone, avg_genre_box_office
    from genreComparison
    order by avg_genre_box_office desc;




--to compare genres find genre_id for Animation, Comdey, Drama and Biography
 select genre_name, id 
 from genre_types 
 where genre_name in ('Animation', 'Comedy', 'Drama', 'Biography')

--Create a common table expression for genre review
with genreReview as (
        select gt.genre_name, mg.movie_id,
        avg(cast(ur.tone as NUMERIC)) as avg_emotional_tone,
        mi.worldwide_box_office
        from genre_types gt
        join movie_genres mg on gt.id = mg.genre_id
        join user_reviews ur on mg.movie_id = ur.movie_id
        join movie_info mi on mi.id = ur.movie_id
        where gt.id in (2, 9, 10, 17)
        group by gt.genre_name, mg.movie_id, mi.worldwide_box_office
    ),
	
		--Create another CTE for genre comparison
    genreComparison as (
        select genre_name,
        avg(avg_emotional_tone) as avg_genre_emotional_tone,
        avg(cast(worldwide_box_office as NUMERIC)) as avg_genre_box_office
        from genreReview 
        group by genre_name
    )
    select genre_name, avg_genre_emotional_tone, avg_genre_box_office
    from genreComparison
    order by avg_genre_box_office desc;
    