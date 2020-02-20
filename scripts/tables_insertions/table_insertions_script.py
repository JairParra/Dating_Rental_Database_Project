# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:37:15 2020

@author: jairp
"""

### 1. Imports 

import time
import numpy
import datetime
import random
import numpy as np 
import pandas as pd
from faker import Faker

##############################################################################

### 2. Setup

# Set up random seeds for reproducibility
np.random.seed(42) 
random.seed(42) 

# Can read from this crap quite easily 
usertable = pd.read_csv('../../data_raw/user_table.csv', encoding='utf8')  # read artificial user table
userdict = usertable.set_index('username').to_dict() # convert to dictionary for easy search 

## Managers 
usernames = list(usertable['username']) # select all usernames 
managers = list(np.random.choice(usernames, size=10, replace=False)) # select 10 managers 

## Mates 
usernames2 = [name for name in usernames if name not in managers] # substract mates
possible_male_mates = [username for username in usernames2 if 
                       userdict['dateofbirth'][username] < '2000-01-01' and 
                       userdict['sex'][username] == 'Male']
possible_female_mates = [username for username in usernames2 if 
                       userdict['dateofbirth'][username] < '2000-01-01' and 
                       userdict['sex'][username] == 'Female']
male_mates = list(np.random.choice(possible_male_mates,size=10,replace=False)) 
female_mates = list(np.random.choice(possible_female_mates,size=10,replace=False)) 
mates = male_mates + female_mates 

## Customers 
customers = [username for username in usernames2 if username not in mates] 

###############################################################################

### 3. Tables Creation 

###############################################################################

## 3.1 create_mate

def create_mate(mates): 
    
    records = [] # list of strings 
    
    nicknames = ["nickname"+str(i) for i in range(len(mates))] # create artificial nicknames
    descriptions = ["description"+str(i) for i in range(len(mates))] # dreate artificial descriptions 
    languages = ["English","French","Eng & French"]
    i = 0 
    
    for username in mates: 
        height = round(random.uniform(1.50, 2.00),2) # generate a random height 
        weight = round(random.uniform(40.00, 75.00))  # generate a random weight 
        hourlyRate = random.randint(50,200) # generate a random hourly rate 
        language = np.random.choice(languages, replace=False)
        
        stmt = "INSERT INTO mate VALUES('{}','{}','{}','{}',{},{},{}); \n".format(username, 
                                       nicknames[i], descriptions[i], language, height, weight, hourlyRate)
        
        records += [stmt]
        i += 1 
        
    return records
        
# create the mates statements 
mates_insertion = create_mate(mates)

 #save the table 
with open("2_mate_insertions.sql", "w") as file: 
    file.writelines(mates_insertion) 
    file.close() 
    
###############################################################################

    
## 3.2  customer_table 
    
def create_customer(customers): 
    
    records = []  # store records
    
    preferences = ["preference"+str(i) for i in range(len(mates))]  # create artificial  preferences
    i = 0 
    
    for username in customers: 
        stmt = "INSERT INTO customer VALUES('{}','{}'); \n".format(username, preferences[i]) 
        records += [stmt]
        i += 1 
        
    return records 

# create the mates statements 
customer_insertion = create_customer(customers)

 #save the table 
with open("3_customer_insertions.sql", "w") as file: 
    file.writelines(customer_insertion) 
    file.close() 
    
    
###############################################################################

    
## 3.3 manager table 
    
def create_manager(managers): 
    
    records = [] # store the records 
    
    # create SQL INSERT statements
    for username in managers: 
        stmt = "INSERT INTO manager VALUES('{}'); \n".format(username) 
        records += stmt 
    
    return records

# create the mates statements 
manager_insertion = create_manager(managers)

 #save the table 
with open("4_manager_insertions.sql", "w") as file: 
    file.writelines(manager_insertion) 
    file.close()  
    
    
###############################################################################


## 3.4 application table 
    
def create_application(mates, managers): 
    """ 
    Will create insertion statements for the application table of the form: 
        INSERT INTO application VALUES(appid, username, aTime, isApproved, mngName)
    respecting the appropriate constraints. 
    @ args: 
        @ mates: a list of mate usernames 
        @ managers: a list of manager usernames
    """
    
    # Note: Number of mates has to be at least the number of managers
    if len(mates) < len(managers): 
        raise ValueError("Cannot have more managers than mates")
        
    
    records = []  # store the records 

    # Choose manager names with replacement
    mngNames = np.random.choice(managers, size=len(mates), replace=True)
    
    # Set up time generation objects 
    fake_time = Faker()
    start_date = datetime.date(year=2018, month=1,day=1) # suppose our business started in 2018
    
    # Approval statuses
    approved = ["True","False"]
    
    # create as many records as mates
    for i in range(len(mates)): 
        
        mateName = mates[i] # choose exactly one matename 
        mngName = mngNames[i] # choose one manager, could be repeated 
        aTime = str(fake_time.date_between(start_date=start_date, end_date='today')) # random date from 2018
        isApproved = np.random.choice(approved) # randomly choose one 
        
        stmt = "INSERT INTO application VALUES({},'{}','{}','{}','{}');\n".format(
                        i+1,mateName, mngName, aTime, isApproved) 
        
        records += [stmt] 
        
    return records 

# create the mates statements 
application_insertion = create_application(mates, managers)

 #save the table 
with open("5_application_insertions.sql", "w") as file: 
    file.writelines(application_insertion) 
    file.close()  

###############################################################################

### 3.5 request table 
    
def create_request(mates, customers, size=20): 
    """ 
    Will create insertion statements for the application table of the form: 
        INSERT INTO application (rid, rinfo, rstatus, custName, mateName, decTime) VALUES( -,-,-,-,-,- )
    respecting the appropriate constraints. 
    @ args: 
        @ mates: a list of mate usernames 
        @ managers: a list of customers
        
    NOTE: A request must have exactly one Mate and exactly one Customer, but 
        a customer can book several Mates, and a single Mate can be booked by several 
        customers (see ER diagram). Request decDate CAN overlap! 
    """
    
    records = []  # store the records 

    # Choose mate and customer names without replacement
    mateNames = np.random.choice(mates, size=size, replace=True) 
    customerNames = np.random.choice(customers, size=size, replace=True)
    
    
    # Set up time generation objects 
    fake_time = Faker()
    start_date = datetime.date(year=2018, month=1,day=1) # suppose our business started in 2018
    request_dates = [fake_time.date_between(start_date=start_date, end_date='today') for i in range(size)] 
    decision_dates = [fake_time.date_between(start_date=request_dates[i], end_date='today') for i in range(size)]
    request_dates = [str(date) for date in request_dates]  # convert back to string format
    decision_dates= [str(date) for date in decision_dates]  # convert back to string format ?
    
    # statuses 
    statuses = ["DEFAULT","rejected","accepted"]
    
    # create size number of records
    for i in range(size): 
        
        rid = i+1            
        rstatus = np.random.choice(statuses, p=[0.20,0.40,0.40]) # choose status randomly 
        custName = customerNames[i] 
        mateName = mateNames[i] 
        rdate = request_dates[i] 
        decDate = decision_dates[i]
        
        # add don't add info for some requests
        if i % 5 != 0: 
            rinfo = "Information" + str(random.randint(1,100))
            stmt = "INSERT INTO request VALUES({},'{}','{}','{}','{}','{}','{}');\n".format(
                rid,rinfo,rstatus,custName,mateName,rdate,decDate)  
        else: 
            stmt = "INSERT INTO request VALUES({},DEFAULT,'{}','{}','{}','{}');\n".format(
                rid,rstatus,custName,mateName,rdate,decDate)              
        
        records += [stmt] 
        
    return records 


# create the request statements 
request_insertion = create_request(mates, customers)

#save the table 
with open("6_request_insertions.sql", "w") as file: 
    file.writelines(request_insertion) 
    file.close()  


###############################################################################

### 3.6 request table 
    
## ** WRITE def create_<table>(): here ** ### 
    
    
## ** WRITE export_sql code in here ** ##
    
    
###############################################################################

### 3.7 invoice table 
    
## ** WRITE def create_<table>(): here ** ### 


## ** WRITE export_sql code in here ** ##

    

###############################################################################

### 3.8 order table 
    
## ** WRITE def create_<table>(): here ** ### 
    
    
## ** WRITE export_sql code in here ** ##



###############################################################################

### 3.9 startTable table 
    
## ** WRITE def create_<table>(): here ** ### 


## ** WRITE export_sql code in here ** ##

    
    
###############################################################################

### 3.10 modify table 
    
## ** WRITE def create_<table>(): here ** ### 
    
    
## ** WRITE export_sql code in here ** ##


###############################################################################

### 3.11 generate table 
    
## ** WRITE def create_<table>(): here ** ### 
    
    
## ** WRITE export_sql code in here ** ##
    
    
    
        
        
    
        
    
    
    
    
    




