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

## list of Managers 
usernames = list(usertable['username']) # select all usernames 
managers = list(np.random.choice(usernames, size=5, replace=False)) # select 5 random managers 

## list of Mates 
usernames2 = [name for name in usernames if name not in managers] # substract mates
possible_male_mates = [username for username in usernames2 if 
                       userdict['dateofbirth'][username] < '2000-01-01' and 
                       userdict['sex'][username] == 'Male']
possible_female_mates = [username for username in usernames2 if 
                       userdict['dateofbirth'][username] < '2000-01-01' and 
                       userdict['sex'][username] == 'Female']  # exclude users who's under 18 //suppose the business started in 2018
male_mates = list(np.random.choice(possible_male_mates,size=5,replace=False)) 
female_mates = list(np.random.choice(possible_female_mates,size=5,replace=False)) # randomly choose 5 male and 5 female from possible list
mates = male_mates + female_mates #as mate

## list of Customers 
customers = [username for username in usernames2 if username not in mates] 


###############################################################################

### 3. Tables Creation 

###############################################################################

## 3.1 create_mate

def create_mate(mates): # argument is a list of mate
    
    records = [] # list of strings 
    
    nicknames = ["nickname"+str(i) for i in range(len(mates))] # create artificial nicknames
    descriptions = ["description"+str(i) for i in range(len(mates))] # dreate artificial descriptions 
    languages = ["English","French","Eng & French"]
    i = 0 
    
    for username in mates: 
        height = round(random.uniform(1.50, 2.00),2) # generate a random height 
        weight = round(random.uniform(55.00, 75.00))  # generate a random weight 
        hourlyRate = random.randint(50,200) # generate a random hourly rate 
        language = np.random.choice(languages, replace=False) # randomly choose one language spoken; modify in language list if needs more than one 
        
        stmt = "INSERT INTO mate VALUES('{}','{}','{}','{}',{},{},{}); \n".format(username, 
                                       nicknames[i], descriptions[i], language, height, weight, hourlyRate)
        # SQL: INSERT INTO mate VALUES('username', 'nickname', 'description', language, height, weight, hR)

        records += [stmt] # save statements to list
        i += 1 
        
    return records
        
# create the list of mates statements 
mates_insertion = create_mate(mates)

#save the table 
with open("2_mate_insertions.sql", "w") as file: 
    file.writelines(mates_insertion) 
    file.close() 
    
#####################################################x##########################
    
## 3.2  customer_table 
    
def create_customer(customers): # argument is a list of customer
    
    records = []  # store records
    
    preferences = ["preference"+str(i) for i in range(len(customers))]  # create artificial  preferences
    i = 0 
    
    for username in customers: 
        stmt = "INSERT INTO customer VALUES('{}','{}'); \n".format(username, preferences[i]) 
         # SQL: INSERT INTO customer VALUES('username', 'preference')

        records += [stmt] # save statements to list
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
    
def create_manager(managers): # argument is a list of manager
    
    records = [] # store the records 
    
    # create SQL INSERT statements
    for username in managers: 
        stmt = "INSERT INTO manager VALUES('{}'); \n".format(username) 
        # SQL: INSERT INTO manager VALUES('username')

        records += [stmt]  # save statements to list
    
    return records

# create the manager statements 
manager_insertion = create_manager(managers)

 #save the table 
with open("4_manager_insertions.sql", "w") as file: 
    file.writelines(manager_insertion) 
    file.close()  
    
###############################################################################

## 3.4 application table 
    
def create_application(mates, managers): # arguments are a list of mate and a list of manager
    
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
    approved = ["Approved","Pending","Rejected"]
    
    # create as many records as mates
    for i in range(len(mates)): 
        
        mateName = mates[i] # choose exactly one matename 
        mngName = mngNames[i] # choose one manager, could be repeated 
        aTime = str(fake_time.date_between(start_date=start_date, end_date='today')) # random date from 2018
        appStatus = np.random.choice(approved) # randomly choose one 
        
        stmt = "INSERT INTO application VALUES({},'{}','{}','{}','{}');\n".format(
                        i+1,mateName, mngName, aTime, appStatus) 
        # SQL: INSERT INTO application VALUES(appid, username, aTime, isApproved, mngName)
        
        records += [stmt]  # save statements to list
        
    return records 

# create the mates statements 
application_insertion = create_application(mates, managers)

 #save the table 
with open("5_application_insertions.sql", "w") as file: 
    file.writelines(application_insertion) 
    file.close()  

###############################################################################

### 3.5 request table 
    
def create_request(mates, customers, size=10): #arguments are a list of mate, a list of customer, and size as integer
    
    records = []  # store the records 

    # Choose mate and customer names without replacement
    mateNames = np.random.choice(mates, size=size, replace=True) 
    customerNames = np.random.choice(customers, size=size, replace=True)
       
    # Set up time generation objects 
    fake_time = Faker()
    start_date = datetime.date(year=2018, month=1,day=1) # suppose our business started in 2018
    request_dates = [fake_time.date_between(start_date=start_date, end_date='today') for i in range(size)] 
    decision_dates = [fake_time.date_between(start_date=request_dates[i], end_date='today') for i in range(size)] # randomly choose set of times
    request_dates = [str(date) for date in request_dates] 
    decision_dates= [str(date) for date in decision_dates]  # convert to string format
    
    # statuses 
    statuses = ["pending","rejected","accepted"]
    
    # rids: we will need this values later
    rids = []
    custnames = [] 
    matenames = []
    
    # create size number of records
    for i in range(size): 
        
        rid = i+1 # rid starts from 1
        rstatus = np.random.choice(statuses, p=[0.30,0.35,0.35]) # choose status randomly 
        rinfo = "Information" + str(random.randint(1,100))  # format
        custName = customerNames[i] 
        mateName = mateNames[i] 
        rdate = request_dates[i] 
        decDate = decision_dates[i]
        
        # add don't add info for some requests
        if i % 6 != 0: 
            stmt = "INSERT INTO request VALUES({},'{}','{}','{}','{}','{}','{}');\n".format(
                rid,rinfo,rstatus,custName,mateName,rdate,decDate)  
            #SQL: INSERT INTO request VALUES(rid, rinfo, rstatus, custName, mateName, decTime)
        else: 
            stmt = "INSERT INTO request VALUES({},'{}',DEFAULT,'{}','{}','{}','{}');\n".format(
                rid,rinfo,custName,mateName,rdate,decDate)              
            #SQL: INSERT INTO request VALUES(rid, rinfo, DEFAULT, custName, mateName, decTime)
        rids += [rid]
        custnames += [custName]
        matenames += [mateName]
        records += [stmt]   # save statements to list
        
    return rids, custnames, matenames, records 

# create the request statements 
rids ,rcustnames, rmatenames, request_insertion = create_request(mates, customers) # note that we have also the rids produced

#save the table 
with open("6_request_insertions.sql", "w") as file: 
    file.writelines(request_insertion) 
    file.close()  
    
###############################################################################

### 3.6 order table 
    
def create_order(rids): #argument is a list of request id

    rids = list(np.random.permutation(rids)) # permute randomly
    size = len(rids)
    records = []  # store the records
    comments = ["comments" + str(i + 1) for i in range(size)]  # create artificial

    # Set up time generation objects
    fake_time = Faker()
    start_date0 = datetime.date(year=2018, month=1, day=1)  # suppose our business started in 2018
    start_dates = [fake_time.date_between(start_date=start_date0, end_date='today') for i in range(size)]

    # statuses
    statuses = ["active", "pending", "complete"]
    
    # return order ids 
    oids = []

    # create size number of records
    for i in range(size):
        
        # collect all relevant values
        oid = i + 1
        start_date = start_dates[i]
        ordstatus = random.choice(statuses)  # choose status randomly
        rid = rids[i] # choose the rid from the input rids
        rate_date = fake_time.date_between(start_date=end_date, end_date='today')
        comment = comments[i]
        rating = round(random.uniform(0.0,5.0), 1)
        
        # some orders will have no rating
        if( i % 3 != 0 ):
            stmt = "INSERT INTO orderTable VALUES ({},'{}','{}',{},'{}','{}',{});\n".format(
                oid, str(start_date), ordstatus, rid, rate_date, comment, rating)
            #SQL: INSERT INTO orderTable VALUES (oid, startDate, ordStatus, rid, ratingDate, comment, rating)
        else:
            stmt = """INSERT INTO orderTable (oid, startDate, ordStatus,rid) 
                VALUES({},'{}','{}','{}');\n""".format(
                oid, str(start_date),  ordstatus,  rid)
            #SQL:  INSERT INTO orderTable (oid, startDate, ordStatus, rid) VALUES (-,-,-,-,-)
            # represent requests without rating
            
        # update return values
        records += [stmt] # save statements to list
        oids += [oid]

    return oids, records

# create the request statements
oids, order_insertion = create_order(rids)

# save the table
with open("7_order_insertions.sql", "w") as file:
    file.writelines(order_insertion)
    file.close()

###############################################################################

### 3.7 invoice table 
    
def create_invoice(customers, oids): # arguments are a list of customer and a list of order id

    size = len(oids)
    oids = list(np.random.permutation(oids))
    records = []  # store the records
    descriptions = ["description" + str(i + 1) for i in range(size)]  # create artificial

    # Set up time generation objects
    fake_time = Faker()
    start_date = datetime.date(year=2018, month=1, day=1)  # suppose our business started in 2018
    due_dates = [fake_time.date_between(start_date=start_date, end_date='today') for i in range(size)]
    due_dates = [str(date) for date in due_dates]

    # Choose mate and customer names without replacement
    customerNames = np.random.choice(customers, size=size, replace=True)

    # statuses
    statuses = ["pending", "paid"]
    methods = ["mastercard", "visa", "E-T", "debit", "paypal", "americanexpress", "applepay"]
    
    # return invoice ids 
    inids = []

    # create size number of records
    for i in range(size):
        
        inid = i + 1  # invoice id 
        oid = oids[i]
        status = random.choice(statuses)  # choose status randomly
        method = random.choice(methods) # choose method randomly
        custName = customerNames[i]
        due_date = due_dates[i]
        amount = round(random.uniform(15.00, 200.00))
        stmt = "INSERT INTO invoice VALUES({},{},'{}','{}','{}','{}','{}','{}');\n".format(
            inid, oid, descriptions[i], due_date, amount, custName, method, status)
        #SQL: INSERT INTO invoice VALUES(inid, oid, description, dueDate, amount,custName , method, status) 

        records += [stmt] # save statements to list
        inids += [inid]

    return inids, records

# create the request statements
inids, invoice_insertion = create_invoice(customers, oids)

# save the table
with open("8_invoice_insertions.sql", "w") as file:
    file.writelines(invoice_insertion)
    file.close()

###############################################################################

### 3.8 startTable table 
def create_startTable(rids, customers, mates): #arguments are a list of request id, a list of customer, and a list of mate

    size = len(rids)
    records = []  # store the records

#    customerNames = np.random.choice(customers, size=size, replace=False)
#    matesNames = np.random.choice(mates, size=size, replace=False) 
    customerNames = customers 
    matesNames = mates 
      
    # Set up time generation objects
    fake_time = Faker()
    start_date0 = datetime.date(year=2018, month=1, day=1)  # suppose our business started in 2018
    start_dates = [fake_time.date_between(start_date=start_date0, end_date='today') for i in range(size)]

    # create size number of records
    for i in range(size):
        start_date = start_dates[i]
        stmt = "INSERT INTO startTable VALUES({},'{}','{}','{}');\n".format(
            rids[i], matesNames[i], customerNames[i],str(start_date))
        #SQL: INSERT INTO startTable VALUES(rid, mateName, custName, startDate)

        records += [stmt] # save statements to list
        
    return records

# create the request statements
# the "r" lists came from the script to create the requests
startTable_insertion = create_startTable(rids, rcustnames,rmatenames)

# save the table
with open("9_startTable_insertions.sql", "w") as file:
    file.writelines(startTable_insertion)
    file.close()
    
###############################################################################

### 3.9 Activity table

def create_activity(managers): # argument is a list of manager

    records = []  # store the records
    
    size = len(managers)
    descriptions = ["description" + str(i + 1) for i in range(size)]  # dreate artificial
    managersNames = np.random.choice(managers, size=size, replace=True)
    aids = []
    
    # create size number of records
    for i in range(size):
        aid = i+1
        stmt = "INSERT INTO activity VALUES({},'{}','{}');\n".format(aid, descriptions[i],managersNames[i])
        #SQL: INSERT INTO activity VALUES(aid, descriptions, managerName)

        records += [stmt] # save statements to list
        aids += [aid] 
        
    return aids, records

# create the request statements
aids,activity_insertion = create_activity(managers)

# save the table
with open("10_activity_insertions.sql", "w") as file:
    file.writelines(activity_insertion)
    file.close()

###############################################################################

### 3.10 modify table
    
def create_modify(managers): # argument is a list of manager
    
    size = len(managers)
    records = []  # store the records
    oids = random.sample(range(1, size + 1), size) #randomly choose order id; all are valid note that #order is larger than #manager
    manager = random.sample(managers, size)

    # create time
    fake_time = Faker()
    start_date = datetime.date(year=2018, month=1, day=1)  # suppose our business started in 2018
    modTimes = [fake_time.date_between(start_date=start_date, end_date='today') for i in range(size)]
    modTimes = [str(t) for t in modTimes] # t stands for time

    # create size number of records
    for i in range(size):
        stmt = "INSERT INTO modification VALUES('{}',{},'{}');\n".format(
            manager[i], oids[i], modTimes[i])
        #SQL: INSERT INTO modification VALUES(managerName, oid, modTimes)

        records += [stmt] # save statements to list

    return records

# create the request statements
modify_insertion = create_modify(managers)

# save the table
with open("11_modify_insertions.sql", "w") as file:
    file.writelines(modify_insertion)
    file.close()
    
###############################################################################

### 3.11 generate table
    
def create_generate(oids, rids): # arguments are a list of oid and a list of request id 
    
    size = len(oids) # 
    records = []  # store the records
    oids = np.random.permutation(oids)
    
    # create size number of records
    for i in range(size):
        oid = oids[i]
        rid = rids[i]
        stmt = "INSERT INTO generate VALUES({},{});\n".format(rid, oid)
        #SQL: INSERT INTO generate VALUES(rid, oid)

        records += [stmt] # save statements to list

    return records

# create the generate statements
generate_insertion = create_generate(oids,rids)

# save the table
with open("12_generate_insertions.sql", "w") as file:
    file.writelines(generate_insertion)
    file.close()

###############################################################################


### 3.12 Schedule table

def create_schedule(oids, aids): #  arguments are a list of order id and a list of activity id
    
    records = []  # store the records
    size = len(oids) # 
    aids = list(np.random.choice(aids, size=size, replace=True))   
    
    # create size number of records
    for i in range(size):
        stmt = "INSERT INTO schedule VALUES({},{});\n".format(aids[i], oids[i])
        #SQL: INSERT INTO schedule VALUES(aid, oid)

        records += [stmt] # save statements to list

    return records


# create the request statements
schedule_insertion = create_schedule(oids, aids)

# save the table
with open("13_schedule_insertions.sql", "w") as file:
    file.writelines(schedule_insertion)
    file.close()
        
    
        
    




