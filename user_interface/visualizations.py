# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:34:57 2020

@author: jairp

NOTE: This part will be finished by Chelly
"""

###############################################################################

### 1. Imports 

import re
import sys
import numpy as np 
import pandas as pd 
import seaborn as sns # easier & prettier visualization 
import matplotlib.pyplot as plt 
from scipy.stats import stats
from util import query_executer ## this is a custom function to execute SQL queries. See README / the util.py file!
sns.set()

###############################################################################

### 2. Functions 

### IMPLEMENT YOUR FUNCTIONS HERE ### 

## NOTE: You can use the query_executer function to execute queries which you can pass as a string. 
##       This function will return a pandas DataFrame so you can plot stuff easily. 
## NOTE 2: Please keep the menu function as is, and create other helper functions to do the visualizations. 
##      Call these from the menu when an option is input :) 


## IDEAS!!! 
    # 1. Distribution of Male/Female current Users for Customers, Mates and Managers , all at the same time 
    # 2. Pairplot and distributions of ages vs. hourly rates for Mates 
    # 3. Distribution of statues for applications: active, rejected, pending
    # 4. Be createive and surprise me!! :) 
    
def visualization_menu(): 
    """
    Provides different visualization options that can be decided via I/O command line interaction
    """
    
    try: 
        ## options loop
        while True: 
            
            login_string = "\n######################################################\n"
            login_string += "              Dabase Visualizations Menu              \n"
            login_string += "######################################################\n"
            login_string += "\nPlease choose one of the available options below:\n"
            login_string += "\t 1. Option 1"
            login_string += "\t 2. Option 2"
            login_string += "\t 3. Option 2"
            login_string += "\t 4. Exit" 
            print(login_string) 
            
            # Read input
            user_input = input()  
            
            # Option cases
            if re.match(r'^1.*', str(user_input)):
                print("Execute option 1") 
            
            elif re.match(r'^2.*', str(user_input)):
                print("Execute option 2")
            
            elif re.match(r'^3.*', str(user_input)):
                print("~Goodbye~")
                break
            else: 
                print("Invalid input") 
                continue
            
            
    except Exception as e: 
        print("I/O error occurred\n")
        print("ARGS:{}\n".format(e.args))
        print("Error: ", e)
        print(e.__traceback__)
        print("Context: ", e.__context__)

###############################################################################

### 3. DEMO (delete when not needed anymore) 

## Executing a query 
stmt = "SELECT * FROM application LIMIT 20;" 
df = query_executer(stmt) # execute query on our database, return results as a dataframe 
print(df) # print query 

## Reading the file
red_wine_df = pd.read_csv('../data_raw/winequality-red.csv', sep = ';')  # Load csv file 
red_wine_df_stats = red_wine_df.drop('quality', axis=1).describe() # describe and obtain stats 
red_wine_df_cols = list(red_wine_df.columns)[:-1] # obtain column names 


## Descriptive Statistics
print("Red wine df shape: {}".format(red_wine_df.shape))  # shape
print("Red wine 'Good' counts: ", red_wine_df['quality'][red_wine_df['quality'] == 1].count() ) # count
print("Red wine 'Bad' counds: ", red_wine_df['quality'][red_wine_df['quality'] == 0].count() )# count 
red_wine_df_stats = red_wine_df.drop('quality', axis=1).describe() # descriptive statistics
print(red_wine_df_stats)


## Common plots  
#plt.figure(1) # enumerate figures 
#plt.title("Plot Title") 
#plt.xlabel("X-axis") 
#plt.ylabel("y-axis")
sns.countplot(red_wine_df['quality']) # countplot 
sns.pairplot(red_wine_df.drop('quality', axis= 1), diag_kind='kde') # pairplot
#plt.savefig('../figs/redwine_countplot.png') # Save a plot 
redwine_corr = red_wine_df.corr()['quality'].drop('quality') # obtain correlations with target 
sns.heatmap(red_wine_df.corr(), cmap='Blues') # heatmap of correlations 
plt.show() # show heatmap  





