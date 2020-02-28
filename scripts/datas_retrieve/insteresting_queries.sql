--1. For customers, they want to find a perfect partner who meets his/her requirements. 
-- Thus customer will search for mates with cireteria
-- Let's imitate a customer who wants to date with a male with height greater than 180cm, weight less than 80kg and age less than 30yrs old.
-- Assume today's date is "2020/02/27"
SELECT username, height, weight, DATEDIFF(year, "2020/02/27", dateOfBirth) AS age 
FROM usertable, mate 
WHERE usertable.username = mate.username;

-- 2. For custmers, they might want to see his/her requests in the past 90days.
-- The return result should include matename, request date as well as request status 
-- Assume today's date is "2020/02/27", this customer's name is Jerry.
SELECT mateName, rdate, rstatus 
FROM request
WHERE custName = 'Jerry' AND DATEDIFF(day, "2020/02/27", rdate) <= 90;

--3. For some reaason, the manager want to know all the people(both mate and customers) who have performed a specific activity on a specific date
-- Find name of custsmer and mates who has performed (which mean order status is complete) activity with "aid== 101" on date "2020/02/27"
SELECT DISTINCT custName AS name, matename
FROM request, ordertable
WHERE request.rid = ordertable.rid 
    AND request.status = "complete" 
    AND request.rid = (
        SELECT rid 
        FROM ordertable, schedule
        WHERE ordertable.oid = schedule.oid AND schedule.aid = 101 AND ordertable.startdate = "2020/02/27";
    )
JOIN 
SELECT DISTINCT mate AS name
FROM request, ordertable
WHERE request.rid = ordertable.rid 
    AND request.status = "complete" 
    AND request.rid = (
        SELECT rid 
        FROM ordertable, schedule
        WHERE ordertable.oid = schedule.oid AND schedule.aid = 101 AND ordertable.startdate = "2020/02/27";
    );

-- 4. A mate want to accept a request. Assume the request id is 101.
UPDATE request 
SET rstatus = "accepted" 
WHERE rid = 101;

-- 5. The manager wants to find out the customers who has not paid for an invoice after the duedate (assume today is "2020/02/27")
-- and send the customer an email. Thus we need to find out email, order id, invoice id, invoice duedate and invoice amount
SELECT email,  oid, inid, invoice.dueDate, invoid.amount
FROM usertable, customer, ordertable, invoice
WHERE invoice.status = "pending" AND invoice.dueDate < "2020/02/27";
