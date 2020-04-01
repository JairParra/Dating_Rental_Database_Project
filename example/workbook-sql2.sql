-- Try to write SQLs on your own, use this as a reference when you are not sure
-- how to run certain queries.
--there are 5 skaters data in the database
SELECT count(*)
FROM skaters
;

SELECT rating
FROM skaters
;
--return how many rating there are
SELECT count(rating)
FROM skaters
;

SELECT count(DISTINCT rating)
FROM skaters
;

SELECT age
FROM skaters
;

--this is for all
SELECT AVG(age)
FROM skaters
;


SELECT age
FROM skaters
WHERE rating = 9
;

SELECT AVG(age)
FROM skaters
WHERE rating = 9
;

--this will cause error?
--reason: 不能用WHERE
SELECT AVG(age)
FROM 
( -- Here "t" is a derived table
 SELECT age
 FROM skaters
 WHERE rating = 9
) t
;

SELECT AVG(age)
FROM 
( -- Here "t" is a derived table
 SELECT age
 FROM skaters
 HAVING rating = 9
) t
;
--This is good
--SELECT AVG(age)
--FROM (SELECT age
-- FROM skaters) t;

SELECT AVG(age), COUNT(*)
FROM skaters
WHERE rating = 9
;

SELECT SUM(rating)
FROM skaters
;

SELECT MAX(rating), MIN(rating)
FROM skaters
;

-- sub query is an aggregation but the outer query is not.
SELECT sname
FROM skaters
WHERE rating = (SELECT MAX(rating) FROM skaters)
;

-- ERROR !!
SELECT sname
FROM skaters
WHERE rating = MAX(rating)
;

-- Grouping ...

SELECT rating, AVG(age)
FROM skaters
GROUP BY rating
;

SELECT rating, AVG(age), COUNT(*)
FROM skaters
GROUP BY rating
;
--SUM(1)
--sum(1) is exactly equivalent to count(*) - it returns a count of all the rows within the group.
--with a title called sum
SELECT rating, AVG(age), MIN(age)
, MAX(age), COUNT(*), SUM(1)
FROM skaters
GROUP BY rating
;

-- ERROR !!
SELECT sname, rating, AVG(age)
FROM skaters
GROUP BY rating
;

--different combination of sname and rating
SELECT sname, rating, AVG(age)
FROM skaters
GROUP BY rating,sname
;

SELECT rating, AVG(age) as avgage
FROM skaters
WHERE rating > 6
GROUP BY rating
ORDER BY avgage
;

--usually the order is the last step
--reading all entries with age larger than 10 then we can do the avg so no problem
SELECT rating, AVG(age)
FROM skaters
WHERE age > 10
GROUP BY rating
ORDER BY rating
;


-- Error !!
SELECT rating, AVG(age)
FROM skaters
GROUP BY rating
WHERE AVG(age) > 11
;
--Notice the order of AVG
SELECT rating, AVG(age)
FROM skaters
GROUP BY rating
HAVING AVG(age) > 11
;


SELECT rating, AVG(age)
FROM skaters
WHERE rating < 10
GROUP BY rating
HAVING AVG(age) > 11
;

SELECT rating, age, count(*)
FROM skaters
GROUP BY rating, age
;

SELECT c.cid, p.sid
FROM competition c, participates p
WHERE c.cid = p.cid
;

--COUNT(*)可以单独被SELECT但是如果有别的东西和他一起select 就必须被group by 这样伴随的东西
SELECT c.cid, COUNT(*) AS numskaters
FROM competition c, participates p
WHERE c.cid = p.cid
GROUP BY c.cid
;

SELECT c.cid, COUNT(*) AS numskaters
FROM competition c, participates p
WHERE c.cid = p.cid
AND c.cid IN ( 101,104)
GROUP BY c.cid
;

SELECT cid, COUNT(*) AS numskaters
FROM
(
  SELECT c.cid, p.sid
  FROM competition c, participates p
  WHERE c.cid = p.cid
  AND c.cid IN ( 101,104)
) t2
GROUP BY cid
;

SELECT c.cid, COUNT(*) AS numskaters
FROM competition c, participates p
WHERE c.cid = p.cid
GROUP BY c.cid
HAVING COUNT(*) >= 2
;

SELECT  AVG (S2.age)
FROM Skaters S2
GROUP BY rating
;

--No Nesting of aggregation
-- Error !! no nesting of AGG operators.
SELECT  MIN (AVG (S2.age))
FROM Skaters S2
GROUP BY rating
;



-- Use derived tables OR Views
SELECT MIN(avgage)
FROM
(
  SELECT  AVG (S2.age) AS avgage
  FROM Skaters S2
  GROUP BY rating
)X
;

SELECT   DISTINCT s.sid, s.sname
FROM  skaters s, participates p
WHERE s.sid = p.sid
;

CREATE VIEW activeSkaters (sid,sname) AS
SELECT DISTINCT s.sid, s.sname
FROM  skaters s, participates p
WHERE s.sid = p.sid
;

SELECT *
FROM activeSkaters
;

DROP VIEW activeSkaters;

CREATE VIEW avgSkaterAges(rating, avgage) AS
SELECT  rating, AVG (S2.age)
FROM Skaters S2
GROUP BY rating
;

SELECT * FROM avgSkaterAges;

SELECT MIN(avgage) FROM avgSkaterAges;

DROP VIEW avgSkaterAges;

-- NULL ....  slides

INSERT INTO skaters VALUES(72, 'katie', NULL, 12);
INSERT INTO skaters VALUES(83, 'Jack', NULL, 11);

SELECT * FROM skaters;

SELECT sname, rating, rating+1 newrating  
FROM skaters;
--where ignore the NULL
SELECT * FROM skaters WHERE rating > 5;

SELECT * FROM skaters WHERE NOT rating > 5;


-- Error !!
--This will run but cause error
--because NULL represent that you dont know
--so no == compare
SELECT * FROM skaters WHERE rating = NULL;

SELECT * FROM skaters WHERE rating IS NULL;

SELECT * FROM skaters WHERE rating IS NOT NULL;

--The COALESCE expression is a syntactic shortcut for the CASE expression. That is, the code COALESCE(expression1,...n) is rewritten by the query optimizer as the following CASE expression:
--CASE  
--WHEN (expression1 IS NOT NULL) THEN expression1  
--WHEN (expression2 IS NOT NULL) THEN expression2  
--In this case rating is not null, keep it
--rating is null- >0
SELECT sname, rating
, COALESCE(rating, 0) modrating, 
COALESCE(rating, 0)+1 newrating
FROM skaters;


SELECT sname, rating
  ,CASE WHEN rating IS NULL THEN 0 ELSE rating END modrating
FROM skaters;

SELECT sname, rating
  ,CASE WHEN rating = 10 THEN rating
	      WHEN rating IS NULL THEN 1
				ELSE rating + 1
	 END modrating
FROM skaters;

-- 3 Valued Logic (slides)

SELECT rating FROM skaters;

-- NULLs are considered same for distnct
--NULL 也是distrinct的
SELECT distinct rating FROM skaters;

SELECT rating, count(*)
FROM skaters
GROUP BY rating
;


SELECT count(*) rating FROM skaters;

SELECT count(rating) rating FROM skaters;
--TODO:????
--SELECT count(distinct rating) rating FROM skaters;

SELECT AVG(rating) FROM skaters;

SELECT AVG(rating),
 AVG(age)
 ,SUM(rating), SUM(age), COUNT(*)
  FROM skaters;


----- INNER JOINS

SELECT s.sid, s.sname, p.cid, p.rank
FROM skaters s, participates p
WHERE s.sid = p.sid
ORDER BY s.sid, p.cid
;

SELECT s.sid, s.sname, p.cid, p.rank
FROM skaters s INNER JOIN participates p
  ON s.sid = p.sid
ORDER BY s.sid, p.cid
;

SELECT s.sid, s.sname, p.cid, p.rank
FROM skaters s INNER JOIN participates p
  ON s.sid = p.sid
  AND p.cid IN ( 101, 103 )
ORDER BY s.sid, p.cid
;

SELECT s.sid, s.sname, p.cid, p.rank
FROM skaters s INNER JOIN participates p
  ON s.sid = p.sid
WHERE p.cid IN ( 101, 103 )
ORDER BY s.sid, p.cid
;
--in this case there is no different between the left outer join and the right outer jjoin 
SELECT s.sid, s.sname, p.cid, p.rank
FROM skaters s LEFT OUTER JOIN participates p
  ON s.sid = p.sid
ORDER BY s.sid, p.cid
;

SELECT s.sid, s.sname, p.cid, p.rank
FROM participates p RIGHT OUTER JOIN  skaters s
  ON s.sid =EXXIS p.sid
ORDER BY s.sid, p.cid
;
SELECT s.sid, s.sname, s.rating, s.age, o.sid
     , o.sname, o.rating, o.age
FROM skaters s FULL OUTER JOIN ourskaters o
  ON s.sid = o.sid
ORDER BY s.sid, o.sid
;

SELECT * FROM skaters ORDER BY sid;

SELECT * FROM ourskaters ORDER BY sid;

SELECT s.sid, s.sname, s.rating, s.age, o.sid
     , o.sname, o.rating, o.age
FROM skaters s FULL OUTER JOIN ourskaters o
  ON s.sid = o.sid
ORDER BY s.sid, o.sid
;
  

