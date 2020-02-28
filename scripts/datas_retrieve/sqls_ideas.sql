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
-- Background: Say system has a bug, the orders has some problem between a certain time if a manager modify the order, the system want to find the cust, mate id to contact and solve the problem for the order)
-- Find all manager, cust, mate usename of order between some time interval

CREATE VIEW timeRequest 
    (oid,rid) AS
SELECT 
    oid,
    rid 
FROM orderTable 
WHERE ((DATE_PART('year', '2018-02-02'::date) - DATE_PART('year',enddate::date)) * 12 + (DATE_PART('month', '2018-02-02'::date) - DATE_PART('month', enddate::date))) <= 10
;

SELECT 
    custname, 
    matename,
    mngname
FROM timeRequest temp
INNER JOIN request r
    ON temp.rid = r.rid 
JOIN modification mod 
    ON mod.oid = temp.oid 
; 


