/*The following script creates all tables for the database, 
and inserts records into them as well*/ 

-- Note keep the DROPs in this order
DROP TABLE IF EXISTS customer CASCADE; 
DROP TABLE IF EXISTS application; 
DROP TABLE IF EXISTS manager CASCADE; 
DROP TABLE IF EXISTS mate CASCADE; -- cascade option will drop dependent tables
DROP TABLE IF EXISTS usertable CASCADE; 
DROP TABLE IF EXISTS request CASCADE; 
DROP TABLE IF EXISTS invoice CASCADE; 
DROP TABLE IF EXISTS orderTable CASCADE; 
DROP TABLE IF EXISTS activity CASCADE;
DROP TABLE IF EXISTS startTable CASCADE;
DROP TABLE IF EXISTS modification CASCADE;
DROP TABLE IF EXISTS generate CASCADE;
DROP TABLE IF EXISTS schedule CASCADE;  

CREATE TABLE usertable --entity
(
    username VARCHAR(50) NOT NULL, 
    password VARCHAR(100) NOT NULL, 
    email VARCHAR(100) UNIQUE NOT NULL, 
    firstname VARCHAR(100) NOT NULL, 
    lastname VARCHAR(100) NOT NULL, 
    sex VARCHAR(100) NOT NULL,
    city VARCHAR(30) NOT NULL, 
    phoneNum INTEGER NOT NULL, 
    dateOfBirth DATE,  -- Can be null, but will control minimum age at application level
    PRIMARY KEY (username)
); 

CREATE TABLE mate --entity ISA user
( 
  username VARCHAR(50) NOT NULL, 
  nickname VARCHAR(50) NOT NULL, 
  description VARCHAR(200) NOT NULL, 
  language VARCHAR(15) NOT NULL, 
  height DECIMAL(3,2) NOT NULL,  --store in  (meters.cm),  check at application level 
  weight DECIMAL(5,2) NOT NULL, -- measure in kg.
  hourlyRate DECIMAL, -- should we change this to decimal? , should check? 
  PRIMARY KEY(username), 
  -- refer to a specific column, restrict and cascade to be explained later
  FOREIGN KEY(username) REFERENCES usertable (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE customer --entity ISA user
(
  username VARCHAR(50) NOT NULL, 
  preferences VARCHAR(100) NOT NULL DEFAULT  'undefined' , 
  PRIMARY KEY(username), 
  FOREIGN KEY(username) REFERENCES usertable (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE manager --entity ISA user
(
  username VARCHAR(50) NOT NULL, 
  PRIMARY KEY(username), 
  FOREIGN KEY(username) REFERENCES usertable (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE application --weak entity of mate
(
  appid SERIAL NOT NULL,  -- application id; auto-increment 
  mateName VARCHAR(50) NOT NULL, --username of mate
  mngName VARCHAR(50) NOT NULL, --manager name(username of manager)
  aDate DATE NOT NULL,  -- application date
  appStatus VARCHAR(20) NOT NULL, -- (Pending, Approved, Rejected)
  PRIMARY KEY(appid, mateName),  
  FOREIGN KEY(mateName) REFERENCES mate (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE, 
  FOREIGN KEY(mngName) REFERENCES manager(username)
    ON DELETE RESTRICT ON UPDATE CASCADE 
); 

-- NOTE: request also need to include the customer name!!!! 
CREATE TABLE request --entity
(
  rid SERIAL NOT NULL, --request id; auto-increment
  rinfo VARCHAR(100) NOT NULL ,  --request information
  rstatus VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending , rejected or accepted 
  custName VARCHAR(50) NOT NULL, -- customer name
  mateName VARCHAR(50) NOT NULL, 
  rdate DATE, -- request time
  decDate DATE, -- decision time 
  PRIMARY KEY (rid), 
  FOREIGN KEY (mateName) REFERENCES mate (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE, 
  FOREIGN KEY (custName) REFERENCES customer (username)
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE orderTable --entity
(
  oid SERIAL NOT NULL, 
  startDate DATE NOT NULL, -- format: 'YYYY-MM-DD'
  ordStatus VARCHAR(20) NOT NULL DEFAULT 'pending', -- {active, pending, complete}
  rid INTEGER NOT NULL,  --request id
  ratingDate DATE, -- can be null if no rating
  comment VARCHAR(100), -- can be null 
  rating DECIMAL(2,1)  -- can be nul  l
    CONSTRAINT rat CHECK( rating > 0.0 AND rating <= 5.0), -- restrict range , add to req. analysis
  PRIMARY KEY (oid), 
  FOREIGN KEY (rid) REFERENCES request(rid)
  -- FOREIGN KEY (inid) REFERENCES invoice (inid)
  -- FOREIGN KEY (custName) REFERENCES request (custName) 
); 

CREATE TABLE invoice --entity
(
  inid SERIAL NOT NULL, --invoice id; auto-increment
  oid INTEGER NOT NULL,  -- order id
  description VARCHAR(100) NOT NULL,
  dueDate DATE NOT NULL, 
  amount DECIMAL(100,2) NOT NULL, 
  custName VARCHAR(50) NOT NULL, --customer name (username of customer)
  status VARCHAR(20) NOT NULL, -- (pending, paid)   
  PRIMARY KEY(inid), 
  FOREIGN KEY(custName) REFERENCES customer (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE, 
  FOREIGN KEY (oid) REFERENCES orderTable (oid) 
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE startTable --relationship between request, mate, and customer
(
    rid INTEGER NOT NULL, --request id
    mateName VARCHAR(50) NOT NULL, --username of mate
    custName VARCHAR(50) NOT NULL, --customer name (username of customer)
    startDate DATE NOT NULL,  --start date
    PRIMARY KEY (rid, mateName, custName) ,
    FOREIGN KEY (mateName) REFERENCES mate(username),
    FOREIGN KEY (custName) REFERENCES customer(username),
    FOREIGN KEY (rid) REFERENCES request(rid)
);

CREATE TABLE activity --entity
(
    aid SERIAL NOT NULL, --activity id; auto-increment
    description VARCHAR(200) NOT NULL UNIQUE,
    mngName VARCHAR(50) NOT NULL, --manager name (username of manager)
    PRIMARY KEY (aid), 
    FOREIGN KEY (mngName) REFERENCES manager(username)
);

CREATE TABLE modification --relationship between manager and order
(
    mngName VARCHAR(50) NOT NULL, --manager name (username of manager)
    oid INTEGER NOT NULL, --order id
    modDate DATE NOT NULL,
    FOREIGN KEY (oid) REFERENCES orderTable(oid),
    FOREIGN KEY (mngName) REFERENCES manager(username),
    PRIMARY KEY (mngName,oid)
);


CREATE TABLE generate --relationship between request and order
(
    rid INTEGER NOT NULL, --request id
    oid INTEGER NOT NULL, --order id
    PRIMARY KEY (rid),  
    FOREIGN KEY (rid )REFERENCES request(rid)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (oid) REFERENCES orderTable(oid)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE schedule --relationship between order and activity
(
    aid INTEGER NOT NULL, --activity id
    oid INTEGER NOT NULL, --order id
    PRIMARY KEY (aid,oid),
    FOREIGN KEY (aid)REFERENCES activity(aid)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (oid) REFERENCES orderTable(oid)
        ON DELETE RESTRICT ON UPDATE CASCADE
);


END