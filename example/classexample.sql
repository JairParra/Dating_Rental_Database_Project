--DROP TABLE participates;
--DROP TABLE skaters;
--DROP TABLE competition;
--DROP TABLE ourSkaters;

CREATE TABLE skaters
(
   sid INTEGER NOT NULL
  ,sname VARCHAR(12)
  ,rating INTEGER
  ,age INTEGER
  ,PRIMARY KEY(sid)
);

INSERT INTO skaters VALUES(28, 'yuppy', 9, 15);
INSERT INTO skaters VALUES(31, 'debby', 7, 10);
INSERT INTO skaters VALUES(22, 'conny', 5, 10);
INSERT INTO skaters VALUES(58, 'lilly', 10, 13);
INSERT INTO skaters VALUES(62, 'susie', 9, 17);

CREATE TABLE competition
(
   cid INTEGER NOT NULL
  ,cdate DATE
  ,ctype VARCHAR(15)
  ,PRIMARY KEY(cid)
);

INSERT INTO competition VALUES(101, '2014-12-13', 'local');
INSERT INTO competition VALUES(103, '2015-01-12', 'regional');
INSERT INTO competition VALUES(104, '2015-01-20', 'local');
INSERT INTO competition VALUES(105, '2016-02-24', 'international');


CREATE TABLE participates
(
   sid INTEGER NOT NULL
  ,cid INTEGER NOT NULL
  ,rank INTEGER
  ,PRIMARY KEY(sid, cid)
  ,FOREIGN KEY(sid) REFERENCES skaters(sid)
  ,FOREIGN KEY(cid) REFERENCES competition(cid)
);

INSERT INTO participates VALUES(31, 101, 2);
INSERT INTO participates VALUES(58, 103, 7);
INSERT INTO participates VALUES(58, 101, 7);
INSERT INTO participates VALUES(58, 104, 1);
INSERT INTO participates VALUES(62, 105, 3);
INSERT INTO participates VALUES(62, 103, 1);



CREATE TABLE ourSkaters
(
   sid INTEGER NOT NULL
  ,sname VARCHAR(12)
  ,rating INTEGER
  ,age INTEGER
  ,PRIMARY KEY(sid)
);

INSERT INTO ourSkaters VALUES(28, 'yuppy', 9, 15);
INSERT INTO ourSkaters VALUES(31, 'debby', 7, 10);
INSERT INTO ourSkaters VALUES(22, 'conny', 5, 10);
INSERT INTO ourSkaters VALUES(92, 'Joan', 9, 11);
INSERT INTO ourSkaters VALUES(98, 'lise', 6, 12);

