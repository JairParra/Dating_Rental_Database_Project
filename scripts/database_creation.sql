/*The following script creates all tables for the database, 
and inserts records into them as well*/ 

-- Note keep the DROPs in this order
DROP TABLE IF EXISTS mate; 
DROP TABLE IF EXISTS customer; 
DROP TABLE IF EXISTS application; 
DROP TABLE IF EXISTS manager; 
DROP TABLE IF EXISTS usertable; 

-- NOTE: Cannot use keyword 'user'
CREATE TABLE usertable
(
    username VARCHAR(50) NOT NULL, 
    password VARCHAR(100) NOT NULL, 
    email VARCHAR(100) NOT NULL, 
    first_name VARCHAR(100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL, 
    sex VARCHAR(100) NOT NULL, 
    city VARCHAR(20) NOT NULL, 
    phoneNum INTEGER NOT NULL, 
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
  hourlyRate INTEGER, -- should we change this to decimal? 
  PRIMARY KEY(username), 
  -- refer to a specific column, restrict and cascade to be explained later
  FOREIGN KEY(username) REFERENCES usertable (username) ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE customer 
(
  username VARCHAR(50) NOT NULL, 
  preferences VARCHAR(100), 
  PRIMARY KEY(username), 
  FOREIGN KEY(username) REFERENCES usertable (username) ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE manager 
(
  username VARCHAR(50) NOT NULL, 
  PRIMARY KEY(username), 
  FOREIGN KEY(username) REFERENCES usertable (username) ON DELETE RESTRICT ON UPDATE CASCADE
); 

CREATE TABLE application 
(
  appid SERIAL NOT NULL,  -- this will auto-increment 
  username VARCHAR(50) NOT NULL, --- NOTE: should switch 'username' to 'mateName'
  aTime DATE NOT NULL, 
  isApproved VARCHAR(20) NOT NULL, -- contains boolean values? 
  mngName VARCHAR(50) NOT NULL, 
  PRIMARY KEY(appid, username), 
  FOREIGN KEY(username) REFERENCES mate ON DELETE RESTRICT ON UPDATE CASCADE, 
  FOREIGN KEY(mngName) REFERENCES manager ON DELETE RESTRICT ON UPDATE CASCADE 
); 

CREATE TABLE request
(
  rid SERIAL NOT NULL,  
  rinfo VARCHAR(100),  
  rstatus VARCHAR(20), -- pending , rejected or accepted 
  mateName VARCHAR(50), 
  decTime DATE, -- decision time 
  PRIMARY KEY (rid), 
  FOREIGN KEY (mateName) REFERENCES mate
)



END