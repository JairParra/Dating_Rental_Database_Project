import time
import numpy
import datetime
import random
import numpy as np 
import pandas as pd
from faker import Faker


if __name__ == "__main__":
    # create the request statements 
    invoice_insertion = create_invoice(customers)

    #save the table 
    with open("7_request_invoice.sql", "w") as file: 
        file.writelines(request_insertion) 
        file.close()  

def create_invoice(customers, size=20): 
    """ 
    Will create insertion statements for the invoice table of the form: 
    inid{}, oid{}, description, dueDate, amount{}, custName , pamount{}, method, status  (pending, paid)   
        INSERT INTO invoice (inid, oid, description, dueDate, amount,custName , pamount, method, status)  VALUES( -,-,-,-,-,- )
    respecting the appropriate constraints. 
    @ args: 
        @ mates: a list of mate usernames 
        @ managers: a list of customers

    NOTE: 
    """

    records = []  # store the records 
    oids = random.sample(range(1,size+1), 20)
    descriptions = ["description"+str(i+1) for i in range(len(size))] # dreate artificial 
    for j in range(size):
        desp.append("description"+(j+1))
        oids = random.sample(range(1,size+1), 20)
    
    # Set up time generation objects 
    fake_time = Faker()
    start_date = datetime.date(year=2018, month=1,day=1) # suppose our business started in 2018
    due_dates = [fake_time.date_between(start_date=start_date, end_date='today') for i in range(size)] 
    due_dates = [str(date) for date in due_dates]

    # Choose mate and customer names without replacement
    customerNames = np.random.choice(customers, size=size, replace=True)
    
    # statuses 
    statuses = ["pending","paid"]
    methods = ["mastercard", "visa","E-T","debit","paypal","americanexpress","applepay"]

    # create size number of records
    for i in range(size): 
        
        inid = i+1            
        status = np.random.choice(statuses, p=[0.70,0.30]) # choose status randomly 
        method = np.random.choice(methods,p=[0.20,0.20,0.10,0.20,0.10,0.10,0.10])
        custName = customerNames[i] 
        due_date = due_dates[i] 
        amount = round(random.uniform(15.00, 200.00)) # generate a random height 
        pamount = round(random.uniform(10.00, amount))  # generate a random weight   
        stmt = "INSERT INTO request VALUES({},{},'{}','{}',{},'{}','{}');\n".format(
                inid,oids[i],descriptions[i],due_date,amount,custName,pamount,method,status)         
        
        records += [stmt] 
        
        
    return records


x