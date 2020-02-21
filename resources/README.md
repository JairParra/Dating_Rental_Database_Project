# resources 

- This directory contains resource scripts for database connections and interactions. These scripts, however, are not final, and might not all be used. 
- Links to resources are also listed here. 

## Connection instructions: 

Server information:  
- host: `comp421.cs.mcgill.ca`
- Linux account name: `cs421g88` 
- password: `<our group's password>`

ex. connection:  
`ssh comp421.mcgill.ca -l cs421g88`  

`password: ********`

`cs421g88@comp421 ~ $bash`

Database information: 
- Once inside the server, connect to `postgresql` as follows: 

`psql cs421` 

`password: <same_as_above>` 

## Database creation: 

- Please run the creation (SQL) scripts in the following order: 

    1. usertable_insertions.sql 
    2. mate_insertions.sql
    3. customer_insertions.sql 
    4. manager_insertions.sql

