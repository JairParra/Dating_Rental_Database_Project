# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:10:14 2020

@author: jairp

Dataset Creator
"""

import time
import numpy
import datetime
import random
import numpy as np 
from faker import Faker


# Table creation functions 

def create_venues_records(start_id, num_records): 
    """
    Creates SQL records for the venues table of the form: 
            INSERT INTO venue VALUES(1,'A',100);
    """
    
    final_stmt = ""
    
    # iterate and create all the records 
    for i in range(start_id, start_id+num_records): 
        
        rand_digits = random.randint(1,2) # generate a random num of 1-2 digits
        rand_zeros = random.randint(1,2) # generate 1-2 zeros 
        rand_num = rand_int(rand_digits, rand_zeros)  # generate rand number
        letters = ['A','B','C'] # to choice from 
        
        # insert 
        final_stmt += "INSERT INTO venue VALUES({},'{}',{});\n".format(i, random.choice(letters), rand_num) 
        
    return final_stmt


def create_schedule_records(num_records, null = 0.30): 
    """
    Creates SQL records for the schedule table of the form: 
        INSERT INTO schedule VALUES(13,'2020-01-19',19,'Pop music'); 
        INSERT INTO schedule VALUES(3,'2020-01-19',18);
        INSERT INTO schedule VALUES(vid,,date,eid,note); 
        
    - "vid" ranges between 1-63
    - "date" ranges between '2010-01-01' - '2020-01-01'
    - "eid" ranges between 1-20
    - 'note' can be whatever
    """
    
    final_stmts = []
    
    # decide if insert a null value 
    place_null = np.random.choice([True, False], num_records, p=[null, (1-null)])
    
    # create random notes
    notes = ["note" + str(i) for i in range(1,100)]
    
    # date generation 
    fake = Faker()  # create faker object 
    start_date = datetime.date(year=2010, month=1,day=1) # create a start date 
    
    # create vid range 
    vid_range = [i for i in range(1,64)]
    
    # Generate the records 
    for i in range(num_records): 
        
        random_vid = np.random.choice(vid_range)
        random_date = str(fake.date_between(start_date=start_date, end_date='+1y')) # generate new date 
        random_eid = random.randint(1,21) 
        random_note = np.random.choice(notes)
        
        insert_null = place_null[i]
        
        if insert_null: 
            final_stmts += ["INSERT INTO schedule VALUES({},'{}',{});\n".format(random_vid, random_date, random_eid)]
        else: 
            final_stmts += ["INSERT INTO schedule VALUES({},'{}',{},'{}');\n".format(random_vid, random_date, random_eid, random_note)] 
            
    return list(set(final_stmts))
    
    
## Helpers


def rand_int(num_digits, zeros=0): 
        
    n = num_digits
    range_start = 10**(n-1)
    range_end = (10**n)-1
    
    return random.randint(range_start, range_end) * 10**zeros


    

## Create venue records 

# obtain some random records 
venues_records = create_venues_records(14, 50) 

with open("insert_venues_values.sql","w") as file: 
    file.write(venues_records) 
    file.close() 
    
    
## Create schedule records  
schedule_records = create_schedule_records(50)

with open("insert_schedule_records.sql","w") as file: 
    file.writelines(schedule_records) 
    file.close() 
    
        