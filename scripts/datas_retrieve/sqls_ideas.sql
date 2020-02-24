--UNFINISHED

--1
-- Background: Say we wanna prompt some mates, while activity 001 is considering not appropriate.
-- Find the all the mate has average rank more than 4.0 between a specific(say one week) who does not have the activity 001.
(SELECT * FROM order WHERE AVG(rating)> 4.0  INTERSECT Schedule oid WHERE aid!=1  )->rid -> mateUsername

--2
-- Background: Say we want to add some reward for those customer who has a great loyalty
-- Find all the customer at least one order with rank, can finish their payment in one day

SELECT * FROM order WHERE CHECK rid NOT NULL -> oid -> invoice table return STARTDATE-PAYDATE<=1


--3
-- Background: Say system has a bug, the orders has some problem between a certain time have problems, we want to find the manager, cust, mate id to contact and solve the problem for the order)

-- Find all manager, cust, mate usename of order between some time interval
SELECT * FROM order WHERE (startDate > '2018-02-02' AND endDate < '2018-05-02')

oid -> rid ->   custName, mateName 
    -> modification -> managerName


--4 && 5 to fill
