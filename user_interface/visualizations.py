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
import util
import numpy as np 
import pandas as pd 
import seaborn as sns # easier & prettier visualization 
import matplotlib.pyplot as plt 
from scipy.stats import stats
# ## this is a custom function to execute SQL queries. See README / the util.py file!

sns.set()

###############################################################################

### 2. Functions 

## NOTE: You can use the query_executer function to execute queries which you can pass as a string. 
##       This function will return a pandas DataFrame so you can plot stuff easily. 
## NOTE 2: Please keep the menu function as is, and create other helper functions to do the visualizations. 
##      Call these from the menu when an option is input :)

def visualization1():
    """
    Distribution of Male/Female current Users for Customers, Mates and Managers
    Rationale: the distribution graph reveal about important info on sex, which might helps
    finding the target users, and for advertisement purpose.
    """

    stmt1 = "SELECT sex,COUNT(m.username) count " \
            " FROM mate m" \
            " JOIN usertable u ON m.username= u.username" \
            " GROUP BY sex;"
    stmt2 = "SELECT sex,COUNT(m.username) " \   
            "FROM customer m" \
            " JOIN usertable u ON m.username= u.username" \
            " GROUP BY sex;"
    stmt3 = "SELECT sex,COUNT(m.username) " \
            "FROM manager m" \
            " JOIN usertable u ON m.username= u.username" \
            " GROUP BY sex;"
    df_a = util.query_executer(stmt1)
    df_b = util.query_executer(stmt2)
    df_c= util.query_executer(stmt3)
    print(df_a)
    print(df_b)
    print(df_c)
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
    plt.title('Histogram of female/male ratio for users')
    plt.xticks(group1 + group2 + group3, ('female', 'male') * 3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig('../figs/visual1.png')


def visualization2():
    """ 
    Visualization_2: Pairplot and distributions of ages vs. hourly rates for Mates 
    Rationale: the pair plot provide the relateness between age and hourly rate, 
    which contributes in finding target user since people tends to find similar age friends
    """

    stmt = "SELECT hourlyRate, date_part('year',age('2020-03-31', dateOfBirth)) age " \
            "FROM mate m" \
            " JOIN usertable u ON m.username= u.username;"
    df = util.query_executer(stmt)
    df["hourlyrate"]=df["hourlyrate"].apply(lambda x: int(x))
    df["age"] = df["age"].apply(lambda x: int(x))
    #print(df.to_numpy())
    #print(df.astype({'hourlyrate': 'int64','age': 'int64'}).dtypes)
    sns_plot= sns.pairplot(df, vars=["age", "hourlyrate"])
    plt.title("Mates age vs. hourly rate")
    sns_plot.savefig('../figs/visual_2.png')

def visualization3():
    """
    Box/Distributional plot of the hourlyRate, mean value/Outliers 
    Rationale：This combination of plots helps the company to monitor the hourly pay. 
    (not overprice) Also, check those outliers to identify the popular ones or abnormal one.
    """

    stmt= "SELECT hourlyRate " \
          "FROM mate;"
    df = util.query_executer(stmt)
    df["hourlyrate"]=df["hourlyrate"].apply(lambda x: int(x))
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})

    # Add a graph in each part
    sns.boxplot(df["hourlyrate"], ax=ax_box, showmeans= True)
    sns.distplot(df["hourlyrate"], ax=ax_hist,kde = True,bins=100)

    # Remove x axis name for the boxplot
    ax_box.set(xlabel='')
    plt.title("Boxplot and distributional plot for hourlyRate")
    plt.xlabel("Mate hourly rate")
    plt.ylabel("Frequency")
    plt.show()
    plt.savefig('../figs/visual_3.png')

def visualization4():
    """
    Stacked Histogram for age interval and activites. The company might be instersted in investigating 
    for a certain age interval, which activities are the most popular. 
    This can help the company to form a better recommendation schema for the website. 
    The age intervals are : 1)20-25 2)25-30 3)30-35
    """

    stmt1 ="SELECT COALESCE(a.aid,a.aid) aid, COALESCE (temp.count,0) count " \
           "FROM activity a LEFT OUTER JOIN " \
           "(SELECT s.aid, COUNT(s.aid) count " \
           "FROM usertable u,invoice i,schedule s " \
           "WHERE  u.username = i.custName " \
           "AND i.oid = s.oid " \
           "AND date_part('year',age('2020-03-31',dateOfBirth))<25 " \
           "GROUP BY s.aid ) temp " \
           "ON a.aid = temp.aid " \
           "ORDER BY aid;"


    stmt2= "SELECT COALESCE(a.aid,a.aid) aid, COALESCE (temp.count,0) count " \
           "FROM activity a LEFT OUTER JOIN " \
           "(SELECT s.aid, COUNT(s.aid) count " \
           "FROM usertable u,invoice i,schedule s " \
           "WHERE  u.username = i.custName " \
           "AND i.oid = s.oid " \
           "AND date_part('year',age('2020-03-31',dateOfBirth))<30 " \
           "AND date_part('year',age('2020-03-31',dateOfBirth))>=25 " \
           "GROUP BY s.aid ) temp " \
           "ON a.aid = temp.aid " \
           "ORDER BY aid;"

    stmt3 = "SELECT COALESCE(a.aid,a.aid) aid, COALESCE (temp.count,0) count " \
           "FROM activity a LEFT OUTER JOIN " \
           "(SELECT s.aid, COUNT(s.aid) count " \
           "FROM usertable u,invoice i,schedule s " \
           "WHERE  u.username = i.custName " \
           "AND i.oid = s.oid " \
           "AND date_part('year',age('2020-03-31',dateOfBirth))<35 " \
           "AND date_part('year',age('2020-03-31',dateOfBirth))>=35 " \
           "GROUP BY s.aid ) temp " \
           "ON a.aid = temp.aid " \
            "ORDER BY aid;"


    stmt4 = "SELECT aid" \
            " FROM activity" \
            " ORDER BY aid;"

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
            width=barWidth, label='25~30')
    # Create green bars (top)
    plt.bar(r, df_c['count'].tolist(), bottom=df_b['count'].tolist(), color='#2d7f5e', edgecolor='white',
            width=barWidth, label='30~35')

    # Custom X axis
    plt.xticks(r, names, fontweight='bold')
    plt.xlabel("Activity id")
    plt.ylabel("Count")
    plt.title("Count of users in activities by age group")
    # Show graphic
    plt.legend()
    plt.show()
    plt.savefig('../figs/visual_4.png')

def visualization5():
    """ 
    Donut Plot of statues for applications: Pending, Approved, Rejected, which helps to monitor managers’ workload.
    """

    stmt = "SELECT appStatus, COUNT(appid) count " \
           "FROM application" \
           " GROUP BY appStatus"
    df = util.query_executer(stmt)

    names = df['appstatus'].to_numpy()

    # Create a circle for the center of the plot
    plt.figure() 
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    plt.pie(df['count'].to_numpy(), labels=names, colors=['red', 'green', 'blue', 'skyblue'],autopct=make_autopct(df['count'].to_numpy()))
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.title("Ratio of status of application")
    plt.show()
    plt.savefig('../figs/visual5.png')
    

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


def visualizations_menu(): 
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
            login_string += "\t 1. Histogram of Ratio of male/female user\n"
            login_string += "\t 2. Pair Plot between age and hourlyrate\n"
            login_string += "\t 3. Box/Distributional Plot for hourlyrate\n"
            login_string += "\t 4. Stacked Bar plot for age and acitivity\n"
            login_string += "\t 5. Donut chart for status of application\n"
            login_string += "\t 6. Exit\n"
            print(login_string) 
            
            # Read input
            user_input = input()  
            
            # Option cases
            if re.match(r'^1.*', str(user_input)):
                title = "\n######################################################\n"
                title += "         Histogram of Ratio of male/female users        \n"
                title += "######################################################\n"
                print(title)
                visualization1()
                continue
                
            
            elif re.match(r'^2.*', str(user_input)):
                title = "\n######################################################\n"
                title += "           Pair Plot between age and hourlyrate        \n"
                title += "######################################################\n"
                print(title)
                visualization2()
                continue
            
            elif re.match(r'^3.*', str(user_input)):
                title = "\n######################################################\n"
                title += "           Pair Plot between age and hourlyrate        \n"
                title += "######################################################\n"
                print(title)
                visualization3()
                continue 
            
            elif re.match(r'^4.*', str(user_input)):
                title = "\n######################################################\n"
                title += "           Pair Plot between age and hourlyrate        \n"
                title += "######################################################\n"
                print(title)
                visualization4()
                continue
            
            elif re.match(r'^5.*', str(user_input)):
                title = "\n######################################################\n"
                title += "           Pair Plot between age and hourlyrate        \n"
                title += "######################################################\n"
                print(title)
                visualization5()
                continue 
            
            elif re.match(r'^6.*', str(user_input)):
                print("Exiting visualizations menu...")
                break   
            
            else: 
                print("--INFO--: Invalid Input")
                continue
            
            
    except Exception as e: 
        print("I/O error occurred\n")
        print("ARGS:{}\n".format(e.args))
        print("Error: ", e)
        print(e.__traceback__)
        print("Context: ", e.__context__)



