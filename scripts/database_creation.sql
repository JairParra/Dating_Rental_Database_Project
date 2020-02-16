/*The following script creates all tables for the database, 
and inserts records into them as well*/ 

DROP TABLE IF EXISTS mate; 
DROP TABLE IF EXISTS usertable; 
DROP TABLE IF EXISTS customer; 

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
  FOREIGN KEY(username) REFERENCES userTable
)

CREATE TABLE customer 
(
  username VARCHAR(50) NOT NULL, 
  preferences VARCHAR(100), 
  PRIMARY KEY(username) 
  FOREIGN KEY(username) REFERENCES userTable
)

END