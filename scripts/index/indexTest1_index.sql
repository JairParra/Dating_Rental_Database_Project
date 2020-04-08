DROP INDEX IF EXISTS i;
CREATE INDEX i ON mate (height);
CLUSTER mate USING i;

EXPLAIN ANALYSE
SELECT mate.username, height, weight, (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', dateofbirth)) AS age 
FROM usertable, mate 
WHERE usertable.username = mate.username AND height > 1.8 AND weight < 80 AND (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', dateofbirth)) < 40;