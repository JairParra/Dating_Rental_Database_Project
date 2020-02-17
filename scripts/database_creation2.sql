/**
* The following table create tables Activity, Start, Modify and Generate
*/

DROP TABLE IF EXISTS activity CASCADE;

CREATE TABLE activity
(
    aid SERIAL NOT NULL,
    oid INTEGER NOT NULL,
    description VARCHAR(200) NOT NULL,
    mngName VARCHAR(50) NOT NULL,
    PRIMARY KEY (aid),
    FOREIGN KEY (oid) REFERENCES orderTable(oid)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (mngName) REFERENCES manager(username)
        ON DELETE RESTRICT ON UPDATE CASCADES
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





