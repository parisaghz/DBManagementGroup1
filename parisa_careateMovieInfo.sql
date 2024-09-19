--author : parisa

--create movie_info
CREATE TABLE movie_info AS
SELECT 
    ROW_NUMBER() OVER () AS id,  
    sales.title AS movie_title, 
    sales.release_date, 
    sales.year AS release_year, 
	sales.genre,
    sales.production_budget, 
    meta.run_time, 
    meta.url
FROM sales
JOIN meta ON sales.title = meta.title;




