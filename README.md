[![Generic badge](https://img.shields.io/badge/Database_Project-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Contributors-4-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/COMP421_Databases_Systems-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Status-Building-<COLOR>.svg)](https://shields.io/)


![](figs/database-blue.png)

# COMP421_Database_Project

Creation from scratch of an database from scratch for a real world application. Step by step, you will design a schema, create a database using DB2/PostgreSQL, populate your database with data, maintain, query and update your data, develop application programs, and implement a user-friendly interface.

## Description 
- The purpose of this application is to introduce a dating system different to any others: a date rental service. Instead of putting time and effort in looking for a date, in which some cases people are not willing or feel unable to put in, we want to offer them the possibility of renting a suitable dating partner with certain desired characteristics. Consider for instance, an event in which going alone would be rather awkward; rent a date of your liking instead! Sometimes people feel lonely and would simply like some companies to do their preferred activities: walking around a park, going to a restaurant or a cinema, talk at a café, etc. We propose an interactive platform in which people can do this easily. 

## Overleaf Project/ Writeup 
- Requirement Analysis & Relational Model translation: https://www.overleaf.com/2273196746cvrhdggbvpfm


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

- Please run the following creation (SQL) scriptsin the following order: 

    1. `table_creation.sql`
    2. `1_usertable_insertions.sql` 
    3. `2_mate_insertions.sql` 
    4. `3_customer_insertions.sql` 
    5. `4_manager_insertions.sql`
    6. `5_application_insertions.sql` 
    7. `6_request_insertions.sql`
    8. `7_order_insertions.sql` 
    9. `8_invoice_insertions.sql` 
    10. `9_startTable_insertions.sql`
    11. `10_activity_insertions.sql` 
    12. `11_modify_insertions.sql` 
    13. `12_generate_insertions.sql` 
    14. `13_schedule_insertions.sql`

where the first script is in `scripts/database_creation/` and the rest are in `scripts/table_insertions/` . 
Script 1 is was randomly generated, subsequent table creation scripts were generated using the `table_insertions_script.py` script.

## ER-diagram 

![](figs/ER_model.png)

## User-interface 
- The relevant files are located under the `user_interface` directory. Files descriptions can be found in the respective README.md
- Currently, application will only be emulated locally, but the intention is that it will eventually be available online as well. For this reason, HTML scripts are also placed as well. 

### Demo (Creating a new user, logging-in ) 
```
python main.py

######################################################
Welcome to the MateRental database!
######################################################

Please choose one of the available options below:
         1. Log-in
         2. Register
         3. Administrator Connection
         4. Visualizations menu
         5. Exit

2
Register:
Please input username: user1
Please enter your email: mfsdsd@fdfds.com
Please input password with 1) 1 Uppercase 2) 1 lowercase 3) at least 8 characters:

Error: Password muss contain:
 1 Uppercase, 1 lowercase, at least 8 characters
Register:
Please input username: fdsf
Please enter your email: ewtew
Make sure you input a valid email!
Register:
Please input username: fdsf
Please enter your email: fsf@fdsf.com
Please input password with 1) 1 Uppercase 2) 1 lowercase 3) at least 8 characters:

First name: fdfds
Lasname: ggf
Sex:
1. Male
2. Female
2
City: gfgdfgdf
Please input your phone number with no spaces or special characters432432432
Date of birth:
year (YYYY): 1995
month (MM): 1
day (DD): 1
*****************************SQL*****************************
INSERT INTO usertable (username, password, email , firstname, lastname, sex, city , phoneNum, dateOfBirth) VALUES ('fdsf', 'Hfdfd789789', 'fsf@fdsf.com', 'fdfds', 'ggf', 'Female', 'gfgdfgdf', 432432432, '1995-01-01') ;
*************************MESSAGES****************************
INSERT 0 1
*****************************SQL*****************************
SELECT * FROM usertable WHERE username='fdsf' ;

***************************OUTPUT****************************
Empty DataFrame
Columns: [username, password, email, firstname, lastname, sex, city, phonenum, dateofbirth]
Index: []
*************************MESSAGES****************************
SELECT 0
--INFO-- : User succesfully created! You can now log-in.
Empty DataFrame
Columns: [username, password, email, firstname, lastname, sex, city, phonenum, dateofbirth]
Index: []
```

## Visualizations 

![](figs/visual_5.png)
