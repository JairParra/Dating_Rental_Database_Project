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
DROP TABLE IF EXISTS modify CASCADE;
DROP TABLE IF EXISTS generate CASCADE;

--***FROM MY NOTES. CASCADE is not really friendly,
--*** MAYBE WE SHOULD USE FORIENGN KEY

-- NOTE: Cannot use keyword 'user'
CREATE TABLE usertable
(
    username VARCHAR(50) NOT NULL, 
    password VARCHAR(100) NOT NULL, 
    email VARCHAR(100) NOT NULL, --UNIQUE
    firstname VARCHAR(100) NOT NULL, 
    lastname VARCHAR(100) NOT NULL, 
    sex VARCHAR(100) NOT NULL, -- ***can be INTEGER 0/1 to control?***
    city VARCHAR(30) NOT NULL, 
    phoneNum INTEGER NOT NULL, --**CHECK if INTEGER can hold 
    dateOfBirth DATE,  -- Can be null, but will control minimum age at application level
    PRIMARY KEY (username)
); 

CREATE TABLE mate 
( 
  username VARCHAR(50) NOT NULL, 
  nickname VARCHAR(50) NOT NULL, 
  description VARCHAR(200) NOT NULL, 
  language VARCHAR(15) NOT NULL, 
  height DECIMAL(3,2),  --store in  (meters.cm),  check at application level  
  weight DECIMAL(5,2), -- measure in kg.
  hourlyRate INTEGER, -- should we change this to decimal? , should check?  ***INTEGER is fine 

  --*** WHY the above does not dequired NOT NULL
  PRIMARY KEY(username), 
  -- refer to a specific column, restrict and cascade to be explained later
  FOREIGN KEY(username) REFERENCES usertable (username) 
  --***FOREIGN KEY(username) REFERENCES usertable 
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE customer 
(
  username VARCHAR(50) NOT NULL, 
  preferences VARCHAR(100), --***DEFUAL: 'undefined'
  PRIMARY KEY(username), 
  FOREIGN KEY(username) REFERENCES usertable (username) 
   --***FOREIGN KEY(username) REFERENCES usertable 
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE manager 
(
  username VARCHAR(50) NOT NULL, 
  PRIMARY KEY(username), 
  FOREIGN KEY(username) REFERENCES usertable (username) 

  --***FOREIGN KEY(username) REFERENCES usertable 
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE application 
(
  appid SERIAL NOT NULL,  -- this will auto-increment 
  username VARCHAR(50) NOT NULL, --- NOTE: should switch 'username' to 'mateName'
  aTime DATE NOT NULL, 
  isApproved VARCHAR(20) NOT NULL, -- ***BIT is common for boolean
  mngName VARCHAR(50) NOT NULL, 
  PRIMARY KEY(appid, username), 
  FOREIGN KEY(username) REFERENCES mate (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE, 
  FOREIGN KEY(mngName) REFERENCES manager(username)
    ON DELETE RESTRICT ON UPDATE CASCADE 
); 

-- NOTE: request also need to include the customer name!!!! 
CREATE TABLE request
(
  rid SERIAL NOT NULL UNIQUE,  
  --*** no need for decalring UNIQUE here
  rinfo VARCHAR(100),   --request information? 
  rstatus VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending , rejected or accepted  ***WHY NOT INTEGER
  custName VARCHAR(50) NOT NULL, -- THIS IS NEW!! see note 
  mateName VARCHAR(50) NOT NULL, 
  decTime DATE, -- decision time --***NOTNULL?
  PRIMARY KEY (rid), 
  FOREIGN KEY (mateName) REFERENCES mate (username)
    ON DELETE RESTRICT ON UPDATE CASCADE, 
  FOREIGN KEY (custName) REFERENCES customer (username)
    ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE invoice
(
  inid SERIAL NOT NULL, 
  oid INTEGER NOT NULL,  -- THIS IS A FOREIGN KEY, will see code right after orderTable
  description VARCHAR(100) NOT NULL,
  dueDate DATE NOT NULL, 
  amount DECIMAL(100,2) NOT NULL, 
  custName VARCHAR(50) NOT NULL, 
  pamount DECIMAL(100,2) NOT NULL, --NOTE: repeated????  
  method VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL, -- (pending, paid)   
  PRIMARY KEY(inid), 
  FOREIGN KEY(custName) REFERENCES customer (username) 
    ON DELETE RESTRICT ON UPDATE CASCADE
); 


-- NOTE1: For this one we need to store both date AND exact time, 
-- so 'odate' is the order date: wthe day the "date" will take place.; 
-- NOTE2: ordStatus != rstatus
-- NOTE3: cannot name this 'order' because it is a keyword
CREATE TABLE orderTable 
(
  oid SERIAL NOT NULL, 
  oStartDate DATE NOT NULL, -- format: 'YYYY-MM-DD'
  --*** oEndDate DATE NOT NULL, -- format: 'YYYY-MM-DD'
  startTime TIME NOT NULL, -- format: '15:00:02'
  endTime TIME NOT NULL, 
  ordStatus VARCHAR(20) NOT NULL DEFAULT 'pending', -- {active, pending, complete}
  rid INTEGER NOT NULL,  --request id 
  inid INTEGER NOT NULL, -- invoice id 
  -- custName VARCHAR(50) NOT NULL, -- CustName IS NOT NEEDED!! 
  ratingDate DATE, -- can be null if no rating
  comment VARCHAR(100), -- can be null 
  rating DECIMAL(2,1) 
    CONSTRAINT rat CHECK( rating > 0.0 AND rating <= 5.0), -- restrict range , add to req. analysis
  PRIMARY KEY (oid), 
  FOREIGN KEY (rid) REFERENCES request(rid),
  FOREIGN KEY (inid) REFERENCES invoice (inid)
  -- FOREIGN KEY (custName) REFERENCES request (custName) 
); 

-- update the actual key 
ALTER TABLE invoice 
  ADD FOREIGN KEY (oid) REFERENCES orderTable (oid) ; 


--- Neijin's updates  

CREATE TABLE activity
(
    aid SERIAL NOT NULL,
    oid INTEGER NOT NULL,
    description VARCHAR(200) NOT NULL,
    --***UNIQUE
    mngName VARCHAR(50) NOT NULL,
    PRIMARY KEY (aid), 
    FOREIGN KEY (oid) REFERENCES orderTable(oid), 
    FOREIGN KEY (mngName) REFERENCES manager(username)
);

-- Note1 :Use starttable not start since start is a keyword
-- Note2 : Add an attribute called startDate
CREATE TABLE startTable
(
    rid INTEGER NOT NULL,
    mateName VARCHAR(50) NOT NULL,
    custName VARCHAR(50) NOT NULL,
    startDate DATE NOT NULL,  --start date
    startTime TIME NOT NULL,
    PRIMARY KEY (mateName, custName) ,
    FOREIGN KEY (mateName) REFERENCES mate(username),
    FOREIGN KEY (custName) REFERENCES customer(username),
    FOREIGN KEY (rid) REFERENCES request(rid)
);

CREATE TABLE modify
(
    mngName VARCHAR(50) NOT NULL,
    oid INTEGER NOT NULL,
    modTime TIME NOT NULL,
    modDate DATE NOT NULL,
    FOREIGN KEY (oid) REFERENCES orderTable(oid),
    FOREIGN KEY (mngName) REFERENCES manager(username),
    PRIMARY KEY (mngName,oid)
);

-- generates request if 
CREATE TABLE generate
(
    rid INTEGER NOT NULL,
    oid INTEGER NOT NULL,
    PRIMARY KEY (rid),  
    FOREIGN KEY (rid )REFERENCES request(rid)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (oid) REFERENCES orderTable(oid)
        ON DELETE RESTRICT ON UPDATE CASCADE
);


END