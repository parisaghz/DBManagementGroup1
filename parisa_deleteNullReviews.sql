--author : Parisa Ghazanfari 500955367
--delete all rows with null value of review text
DELETE FROM user_reviews
WHERE TRIM(review_text) = ''; 


DELETE FROM expert_reviews
WHERE TRIM(review_text) = ''; 