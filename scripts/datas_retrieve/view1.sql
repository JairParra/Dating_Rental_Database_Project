--1 VIEW
--Background: For customers they might want to find the mate with higher rank.
--Find the all the mate has average rank more than 4.0 
CREATE VIEW mateRating1 (matename,rating) AS
(SELECT matename, rating
FROM 
(
    SELECT rid, rating 
    FROM orderTable
) as temp, request WHERE temp.rid=request.rid) 
;

CREATE VIEW mateRating2(matename,average) AS
SELECT matename, AVG(rating) as average FROM mateRating1 GROUP BY matename;


SELECT matename FROM mateRating2 WHERE Average > 4.0;
