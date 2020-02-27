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
userdict = usertable.set_index('username').to_dict()  # convert to dictionary for easy search

## Managers
usernames = list(usertable['username'])  # select all usernames
managers = list(np.random.choice(usernames, size=10, replace=False))  # select 10 managers

## Mates
usernames2 = [name for name in usernames if name not in managers]  # substract mates
possible_male_mates = [username for username in usernames2 if
                       userdict['dateofbirth'][username] < '2000-01-01' and
                       userdict['sex'][username] == 'Male']
possible_female_mates = [username for username in usernames2 if
                         userdict['dateofbirth'][username] < '2000-01-01' and
                         userdict['sex'][username] == 'Female']
male_mates = list(np.random.choice(possible_male_mates, size=10, replace=False))
female_mates = list(np.random.choice(possible_female_mates, size=10, replace=False))
mates = male_mates + female_mates

## Customers
customers = [username for username in usernames2 if username not in mates]

###############################################################################

### 3.10 Activity table

def create_activity(managers, size=10):
    #aid, description, mngName

    records = []  # store the records

    descriptions = ["description" + str(i + 1) for i in range(size)]  # dreate artificial
    managersNames = np.random.choice(managers, size=size, replace=True)
    # create size number of records
    for i in range(size):
        aid = i+1
        stmt = "INSERT INTO activity VALUES({},'{}','{}');\n".format(aid, descriptions[i],managersNames[i])
        records += [stmt]
    return records

# create the request statements
activity_insertion = create_activity(managers)

# save the table
with open("10_activity_insertions.sql", "w") as file:
    file.writelines(activity_insertion)
    file.close()














