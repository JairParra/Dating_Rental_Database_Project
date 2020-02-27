[![Generic badge](https://img.shields.io/badge/Database_Project-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Contributors-4-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/COMP421_Databases_Systems-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Status-<Building>.svg)](https://shields.io/)


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

- Please run the creation (SQL) scripts in the following order: 

    1. `table_creation.sql` 
    2. `1_usertable_insertions.sql` 
    3. `2_mate_insertions.sql` 
    4. `3_customer_insertions.sql` 
    5. `4_manager_insertions.sql`
    6. `5_application_insertions.sql` 
    7. `6_request_insertions.sql`

where the first script is in `scripts/database_creation/` and the rest are in `scripts/table_insertions/` 

## Announcements 
- Group on MyCourses: 88 
- Languages used: Java, Python?, PostgreSQL, HTML/CSS/Javascript?


## ER-diagram 

![](figs/ER_model.png)

## User-interface 
- Building 
