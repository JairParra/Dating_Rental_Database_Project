--1. For customers, they want to find a perfect partner who meets his/her requirements. 
-- Thus customer will search for mates with cireteria
-- Let's imitate a customer who wants to date with a male with height greater than 180cm, weight less than 80kg and age less than 40yrs old.
-- Assume today's date is "2020/02/27"
SELECT mate.username, height, weight, (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', dateofbirth)) AS age 
FROM usertable, mate 
WHERE usertable.username = mate.username AND height > 1.8 AND weight < 80 AND (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', dateofbirth)) < 40;

-- 2. For customers, they might want to see his/her requests in the past 90days.
-- The return result should include matename, request date as well as request status 
-- Assume today's date is "2020/02/27", this customer's name is bmatousl.
SELECT mateName, rdate, rstatus 
FROM request
WHERE custName = 'chysom17' AND (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', rdate)) <= 90;

--3. For some reason, the manager want to know all the people(both mate and customers) who have performed a specific activity on a specific date
-- Find name of custsmer and mates who has performed (which mean order status is complete) activity with "aid=1" on date "2020/02/27"
SELECT DISTINCT custName AS name
FROM request, ordertable
WHERE request.rid = ordertable.rid 
    AND ordertable.ordStatus = 'complete'
    AND request.rid = (
        SELECT rid 
        FROM ordertable, schedule
        WHERE ordertable.oid = schedule.oid AND schedule.aid = 3 AND ordertable.startdate = '2020-02-14'
)
UNION
SELECT DISTINCT matename AS name
FROM request, ordertable
WHERE request.rid = ordertable.rid 
    AND ordertable.ordStatus = 'complete'
    AND request.rid = (
        SELECT rid 
        FROM ordertable, schedule
        WHERE ordertable.oid = schedule.oid AND schedule.aid = 3 AND ordertable.startdate = '2020-02-14'
);


-- 4. The manager wants to find out the customers who has not paid for an invoice after the duedate (assume today is "2020/02/27")
-- and send the customer an email. Thus we need to find out email, order id, invoice id, invoice duedate and invoice amount
SELECT email, ordertable.oid, inid, invoice.dueDate, invoice.amount
FROM usertable, customer, ordertable, request, invoice
WHERE 
            usertable.username = customer.username 
            AND customer.username = request.custName
            AND ordertable.rid = request.rid
            AND ordertable.oid = invoice.oid
            AND invoice.status = 'pending' 
            AND invoice.dueDate < '2020-02-27';

-- 5. Find the most popular activity among male customers with age between 25-35 years old inclusive
SELECT aid, count(*)
FROM schedule
WHERE aid = (
    SELECT MAX(count)
    FROM (
        SELECT count(*) AS count
        FROM usertable, customer, request, ordertable, schedule
        WHERE usertable.username = customer.username 
            AND customer.username = request.custName
            AND ordertable.rid = request.rid
            AND ordertable.oid = schedule.oid
            -- AND usertable.sex = 'male'
            AND (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', dateofbirth)) >=10
            -- AND (DATE_PART('year', '2020-02-27'::date) - DATE_PART('year', dateofbirth)) <=40
        GROUP BY aid 
    ) AS max
)
GROUP BY aid




