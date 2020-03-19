INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(1,'2019-01-30','active','10');
INSERT INTO orderTable VALUES (2,'2018-02-01','complete',30,'2019-02-12','comments2',3.8);
INSERT INTO orderTable VALUES (3,'2019-06-16','active',2,'2020-01-31','comments3',3.3);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(4,'2018-01-07','complete','20');
INSERT INTO orderTable VALUES (5,'2019-06-10','complete',25,'2019-08-10','comments5',4.4);
INSERT INTO orderTable VALUES (6,'2019-08-02','pending',28,'2020-01-07','comments6',4.8);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(7,'2018-01-14','complete','7');
INSERT INTO orderTable VALUES (8,'2019-08-21','complete',8,'2019-09-25','comments8',1.0);
INSERT INTO orderTable VALUES (9,'2018-05-15','pending',19,'2020-01-03','comments9',2.0);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(10,'2019-08-08','complete','24');
INSERT INTO orderTable VALUES (11,'2018-08-01','pending',6,'2018-12-23','comments11',4.5);
INSERT INTO orderTable VALUES (12,'2018-06-27','pending',23,'2019-08-26','comments12',0.6);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(13,'2020-01-14','active','17');
INSERT INTO orderTable VALUES (14,'2019-05-06','active',14,'2020-02-28','comments14',2.9);
INSERT INTO orderTable VALUES (15,'2018-08-01','active',1,'2019-01-01','comments15',2.9);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(16,'2020-02-18','active','9');
INSERT INTO orderTable VALUES (17,'2020-02-28','complete',27,'2020-03-11','comments17',0.3);
INSERT INTO orderTable VALUES (18,'2018-09-28','active',18,'2019-07-24','comments18',4.5);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(19,'2019-07-13','pending','3');
INSERT INTO orderTable VALUES (20,'2019-04-10','active',4,'2019-06-01','comments20',1.4);
INSERT INTO orderTable VALUES (21,'2019-02-10','pending',5,'2019-05-31','comments21',1.1);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(22,'2018-09-18','active','11');
INSERT INTO orderTable VALUES (23,'2019-07-17','complete',26,'2019-12-24','comments23',2.9);
INSERT INTO orderTable VALUES (24,'2018-06-29','active',22,'2020-02-07','comments24',3.9);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(25,'2018-04-26','pending','16');
INSERT INTO orderTable VALUES (26,'2018-01-04','active',21,'2019-07-16','comments26',3.3);
INSERT INTO orderTable VALUES (27,'2019-09-07','pending',15,'2020-02-15','comments27',2.1);
INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES(28,'2018-10-30','pending','29');
INSERT INTO orderTable VALUES (29,'2018-01-10','active',13,'2018-06-01','comments29',3.4);
INSERT INTO orderTable VALUES (30,'2019-02-23','complete',12,'2019-05-05','comments30',0.5);

SELECT * FROM ordertable LIMIT 10; 

