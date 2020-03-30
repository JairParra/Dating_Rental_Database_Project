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
import user_interface.util as util
# ## this is a custom function to execute SQL queries. See README / the util.py file!

sns.set()

###############################################################################

### 2. Functions 

## NOTE: You can use the query_executer function to execute queries which you can pass as a string. 
##       This function will return a pandas DataFrame so you can plot stuff easily. 
## NOTE 2: Please keep the menu function as is, and create other helper functions to do the visualizations. 
##      Call these from the menu when an option is input :)

def visualization1():
    # 1. Distribution of Male/Female current Users for Customers, Mates and Managers , all at the same time
    # Bussiness idea 1: many help balance male/female user ,find the target user, advertisement user
    stmt1 = "SELECT sex,COUNT(m.username) count " \
            "FROM mate m" \
            "JOIN usertable u ON m.username= u.username" \
            "GROUP BY sex;"
    stmt2 = "SELECT sex,COUNT(m.username) " \
            "FROM customer m" \
            "JOIN usertable u ON m.username= u.username" \
            "GROUP BY sex;"
    stmt3 = "SELECT sex,COUNT(m.username) " \
            "FROM manager m" \
            "JOIN usertable u ON m.username= u.username" \
            "GROUP BY sex;"
    df_a = util.query_executer(stmt1)
    df_b = util.query_executer(stmt2)
    df_c= util.query_executer(stmt3)

    n_groups = 3
    fig, ax = plt.subplots()
    # parameter for drawing
    bar_width = 0.35
    opacity = 0.8
    index = 0;

    group1 = [index, index + bar_width]
    rects1 = plt.bar(group1, df_a['count'].to_numpy(), bar_width,
                     alpha=opacity,
                     color='b',
                     label='mate')

    group2 = list(map(lambda x: x + 1, group1))
    rects2 = plt.bar(group2, df_b['count'].to_numpy(), bar_width,
                     alpha=opacity,
                     color='g',
                     label='customer')

    group3 = list(map(lambda x: x + 1, group2))
    rects3 = plt.bar(group3, df_c['count'].to_numpy(), bar_width,
                     alpha=opacity,
                     color='y',
                     label='manager')

    plt.xlabel('Sex')
    plt.ylabel('Count')
    plt.title('Historgram of female/male ratio')
    plt.xticks(group1 + group2 + group3, ('female', 'male') * 3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig('../figs/visual1.png')

def visualization2():
    # 2. Pairplot and distributions of ages vs. hourly rates for Mates
    stmt = "SELECT m.username, hourlyRate, sex  " \
            "FROM mate m" \
            "JOIN usertable u ON m.username= u.username;"
    df = util.query_executer(stmt)
    sns_plot= sns.pairplot(df, vars=["sex", "hourlyRate"])
    sns_plot.savefig('../figs/visual2.png')

def visualization3():
    # Bussiness idea 2: Distribution of the hourly pay, mean value/Outliers- monitorning usage, to check
    # the hourly pay is not overprice. Also, check those outliers to better understand user behaviours.
    stmt= "SELECT username, hourlyRate " \
          "FROM mate;"
    df = util.query_executer(stmt)
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})

    # Add a graph in each part
    sns.boxplot(df["hourlyRate"], ax=ax_box)
    sns.distplot(df["hourlyRate"], ax=ax_hist)

    # Remove x axis name for the boxplot
    ax_box.set(xlabel='')
    plt.show()
    plt.savefig('../figs/visual3.png')

def visualization4():
    # Bussiness idea 3: check which age interval, most interested in which activities, better recommandations
    # Age interval :  1)<25 applicaiton should handle >=20 2) 25~30 3) 30~35
    stmt1 = "SELECT a.aid, COALESCE(count,0) count " \
            "FROM activity OUTER LEFT JOIN (" \
                " SELECT aid,COUNT(aid) count" \
                "FROM usertable u,invoice i,schedule s" \
                "WHERE  u.username = i.custName" \
                "   AND i.oid = s.oid" \
                "   AND age<25" \
                "GROUP BY aid) temp " \
            "ON a.aid = temp.aid" \
            "GROUP BY aid;"

    stmt2 = "SELECT a.aid, COALESCE(count,0) count" \
            "FROM activity OUTER LEFT JOIN (" \
                "SELECT  aid, COUNT(aid) count"\
                "FROM usertable u,invoice i,schedule s" \
                "WHERE  u.username = i.custName" \
                "   AND i.oid = s.oid" \
                "   AND age>=25" \
                "   AND age<30" \
                "GROUP BY aid) temp" \
            "ON a.aid = temp.aid" \
            "OURDER BY aid;"
    stmt3 = "SELECT a.aid, COALESCE(count,0) count" \
            "FROM activity OUTER LEFT JOIN (" \
                "SELECT aid, COUNT(aid) count" \
                "FROM usertable u,invoice i,schedule s" \
                "WHERE  u.username = i.custName" \
                "   AND i.oid = s.oid" \
                "   AND age>=30" \
                "GROUP BY aid) temp" \
            "ON a.aid = temp.aid" \
            "ORDER BY aid;"
    stmt4 = "SELECT aid" \
            "FROM activity" \
            "ORDER BY aid;"

    df_a = util.query_executer(stmt1)
    df_b = util.query_executer(stmt2)
    df_c = util.query_executer(stmt3)
    df_d = util.query_executer(stmt4)

    # The position of the bars on the x-axis
    r = range(len(df_d['aid'].tolist()))

    # Names of group and bar width
    names = df_d['aid'].tolist()
    barWidth = 1

    # Create brown bars
    plt.bar(r, df_a['count'].tolist(), color='#7f6d5f', edgecolor='white', width=barWidth, label='<25')
    # Create green bars (middle), on top of the firs ones
    plt.bar(r, df_b['count'].tolist(), bottom=df_a['count'].tolist(), color='#557f2d', edgecolor='white',
            width=barWidth, label='25~40')
    # Create green bars (top)
    plt.bar(r, df_c['count'].tolist(), bottom=df_b['count'].tolist(), color='#2d7f5e', edgecolor='white',
            width=barWidth, label='>40')

    # Custom X axis
    plt.xticks(r, names, fontweight='bold')
    plt.xlabel("group")

    # Show graphic
    plt.legend()
    plt.show()
    plt.savefig('../figs/visual4.png')

def visualization5():
    # 5. Distribution of statues for applications: Pending, Approved, Rejected

    stmt = "SELECT appStatus, COUNT(appid) count " \
           "FROM applicaiton" \
           "GROUP BY appStatus"
    df = util.query_executer(stmt)

    names = df['appStatus'].to_numpy()

    # Create a circle for the center of the plot
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    plt.pie(df['count'].to_numpy(), labels=names, colors=['red', 'green', 'blue', 'skyblue'])
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.show()
    plt.savefig('../figs/visual5.png')
    
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

            login_string += "\t 1. Ratio of male/female user"
            login_string += "\t 2. Distribution of hourly payment"
            login_string += "\t 3. Age/Activities Plot"
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
def demo():
## Executing a query 
    stmt = "SELECT * FROM application LIMIT 20;"
    df = util.query_executer(stmt) # execute query on our database, return results as a dataframe
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
    #plt.savefig('../figs/redwine_countplot.png') # Save a sex plot
    redwine_corr = red_wine_df.corr()['quality'].drop('quality') # obtain correlations with target
    sns.heatmap(red_wine_df.corr(), cmap='Blues') # heatmap of correlations
    plt.show() # show heatmap

if __name__ == '__main__':
    visualization1()



