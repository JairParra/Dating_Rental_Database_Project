--1 VIEW
-- Background: For customers they might want to find the mate with higher rank.
-- Find the all the mate has average rank more than 4.0 
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


SELECT matename FROM mateRating2 WHERE Average > 4.0

--2View
-- Background: Say system has a bug, the orders has some problem between a certain time have problems, the manager want to find the cust, mate id to contact and solve the problem for the order)
-- Find all manager, cust, mate usename of order between some time interval

--CREATE VIEW timeRequest(custName, mateName) AS
--SELECT rid FROM orderTable WHERE DATEDIFF(day, --'2018/03/05', endDate) <= 100
--;
--SELECT custName, mateName FROM timeRequest as temp, request WHERE temp.rid=request.rid

