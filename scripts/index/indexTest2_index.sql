DROP INDEX IF EXISTS i;
CREATE INDEX i ON request (custName);
CLUSTER request USING i;

EXPLAIN ANALYSE
SELECT mateName, rdate, rstatus 
FROM request
WHERE custName = 'chysom17' AND (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', rdate)) <= 90;