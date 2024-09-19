--author : parisa

-- split movie name from url in user_review_source
select * from user_review_source;

ALTER TABLE user_review_source
ADD COLUMN movie_name text;

UPDATE user_review_source
SET movie_name = SPLIT_PART(url, '/', 5);


-- split movie name from url in expert_review_source
select * from expert_review_source;

ALTER TABLE expert_review_source
ADD COLUMN movie_name text;

UPDATE expert_review_source
SET movie_name = SPLIT_PART(url, '/', 5);
