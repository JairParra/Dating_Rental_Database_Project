# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 19:23:34 2020

@author: jairp
"""

import re
from datetime import date

from util import query_executer
from login import LoginSession # parent class 

# other
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'
STRONG_EMAIL = r'[A-Za-z0-9@#$%^&+=]{8,}'

##############################################################################

### Class definition ### 
        
class ManagerSession(LoginSession):
    """ 
    Inherits from the LoginSession class and implements extra methods
    appropriate to Manager Functions and permissions. 
    """ 
    def __init__(self, loginsession, newuser=False, verbose=True): 
        """
        @args: 
            @ loginsession: an instance of the LoginSession class. Will throw an error 
            if wrong type input. 
        """
        # Initialize and typecheck
        super().__init__(newuser=newuser, verbose=verbose) # call super constructor 
        if not isinstance(loginsession, LoginSession):
            raise TypeError("Constructor argument should be of type 'LoginSession'")
            
        # Copy all attributes from argument instance
        self.login_resp = loginsession.login_resp 
        self.usertype = loginsession.usertype 
        self.usertype_vals = loginsession.usertype_vals 
                
        print("MANAGER LOGIN: \n", self.login_resp) 
        print("MANAGER TYPE: \n", self.usertype)
        print("MANAGER VALUES: \n", self.usertype_vals)
        
        self.menu() # display appropriate optins menu
        
        
    def menu(self): 
        """
        Customized Menu with Manager Options
        """ 
        
        while True: 
            menu_string = "\n######################################################\n"
            menu_string += "                     Options Menu                      \n"
            menu_string += "######################################################\n"
            menu_string += "\nPlease choose one of the available options below:\n"
            menu_string += "\t 1. Review Mate Application\n"  
            menu_string += "\t 2. Modify Order\n"
            menu_string += "\t 3. Overview Activity\n"
            menu_string += "\t 4. Exit"
            print(menu_string) 
            
            mgr_input = input() 
            
            if re.match(r'^1.*', str(mgr_input)): 
                print("Review application") 
                
            elif re.match(r'^2.*', str(mgr_input)): 
                print("Modify Order")
            
            elif re.match(r'^3.*', str(mgr_input)): 
                print("Overview Activity")
                
            elif re.match(r'^4.*', str(mgr_input)): 
                print("Exiting...")
                break
            else: 
                print("Invalid Input")
                
        
        def review_application(self): 
            """ 
            Allows the manager to see some application from a customer to a mate
            """
            try:

                while True:
                    menu_string = "\n######################################################\n"
                    menu_string += "                Look for an Application                \n"
                    menu_string += "######################################################\n"
                    menu_string += "1. See all applications\n"
                    menu_string += "2. Custom search\n"
                    menu_string += "3. Exit\n"
                    print(menu_string)

                    sub_input1 = input()

                    if re.match(r'^1', str(sub_input1)):

                        ## Manager only allow to see the order in his charge
                        print("**You username**")
                        mngName = input()

                        stmt = "SELECT *"
                        stmt += "FROM application\n"
                        stmt += "WHERE mngName=" +mngName +";"
                        query_executer(stmt) # execute and display query and result

                    elif re.match(r'^2', str(sub_input1)):

                        ## 1. Custom search according to different attributes
                        print("**You username**")
                        mngName = input()
                        print("Custom search: Choose custom preferences for your application :) ")

                        ### 1.1 status:Pending, Approved, Rejected
                        print("Status:\n 1) Pending 2)Approved 3)Rejected")
                        if re.match(r'^1', str(input())):
                            status = "pending"
                        elif re.match(r'^2', str(sub_input1)):
                            status = "approved"
                        elif re.match(r'^3', str(sub_input1)):
                            status = "rejected"
                        else:
                            print("Invalid input")
                            continue

                        stmt = "SELECT *\n"
                        stmt += "FROM aplication "
                        stmt += "WHERE mngName=" + mngName + "\n"
                        stmt += "AND status=" + status+";"


                    elif re.match(r'^3', str(sub_input1)):
                        print("Exit")
                        break
                    else:
                        print("Invalid Input")

            except Exception as e:
                print("I/O error occurred\n")
                print("ARGS:{}\n".format(e.args))
                print("Error: ", e)
                print(e.__traceback__)
                print("Context: ", e.__context__)
            
        def modify_order(self): 
            """ 
            Allows the manager to modify an existing order 
            """
            try:

                while True:
                    menu_string = "\n######################################################\n"
                    menu_string += "                     Modify the Order                  \n"
                    menu_string += "######################################################\n"
                    menu_string += "1. Update\n"
                    menu_string += "2. Delete\n"
                    menu_string += "3. Insert\n"
                    menu_string += "4. Exit\n"
                    print(menu_string)

                    sub_input1 = input()

                    if re.match(r'^1', str(sub_input1)):

                        # Check the value that manager want to update
                        # Insert the new record in to the modification table
                        print("Enter the id of order you want to modified")
                        oid = str(input())
                        print("Enter the your user name")
                        mgnName = str(input())
                        print("Enter the status of order you want to change 1)active 2)pending 3) complete")
                        if re.match(r'^1', str(input())):
                            status = "active"
                        elif re.match(r'^2', str(sub_input1)):
                            status = "pending"
                        elif re.match(r'^3', str(sub_input1)):
                            status = 'complete'
                        else:
                            print("Invalid input")
                            continue
                        stmt = "UPDATE order\n"
                        stmt +="SET ordStatus=" + status+"\n"
                        stmt += "WHERE oid=" +oid +";"
                        today = date.today()
                        d1= today.strftime("%Y-%m/%d")
                        query_executer(stmt)  # execute and display query and result
                        stmt1 = "INSERT INTO modification VALUES("+mgnName+"," +oid+","+ d1 +";"
                        query_executer(stmt1)
                    elif re.match(r'^2', str(sub_input1)):
                        print("Enter the id of order you want to modified")
                        oid = str(input())
                        stmt = "DELETE FROM order WHERE oid="+oid+";"
                        query_executer(stmt)
                    elif re.match(r'^3', str(sub_input1)):
                        print("Enter the id of order you want to insert")
                        oid = str(input())
                        print("Enter the start day in from of YY-MM-DD")
                        startDate = str(input())
                        if re.match(r'^1', str(input())):
                            status = "active"
                        elif re.match(r'^2', str(sub_input1)):
                            status = "pending"
                        elif re.match(r'^3', str(sub_input1)):
                            status = 'complete'
                        else:
                            print("Invalid input")
                            continue
                        print("Enter the id of order you want to insert")
                        rid = str(input())
                        # Those attribute should be insert by costumer
                        # print("Enter the rating day in from of YY-MM-DD")
                        # ratingDate = str(input())
                        # print("Enter the comment")
                        # comment = str(input())
                        # print("Enter the rating")
                        # rating = str(input())
                        stmt = "INSERT INTO orderTable (oid, startDate, ordStatus,rid) " \
                               "VALUES("+oid+"," +startDate+","+status+","+rid+");"
                        query_executer(stmt)

                    elif re.match(r'^4', str(sub_input1)):
                        print("Exit")
                        break
                    else:
                        print("Invalid Input")

            except Exception as e:
                print("I/O error occurred\n")
                print("ARGS:{}\n".format(e.args))
                print("Error: ", e)
                print(e.__traceback__)
                print("Context: ", e.__context__)

            
        def overview_activity(self): 
            """ 
            Allows the manager to see and modify some activity (insert, delete, udpate)
            """
            try:

                while True:
                    menu_string = "\n######################################################\n"
                    menu_string += "                Overview for an Activity                \n"
                    menu_string += "######################################################\n"
                    menu_string += "1. Update\n"
                    menu_string += "2. Delete\n"
                    menu_string += "3. Insert\n"
                    menu_string += "4. Exit\n"
                    print(menu_string)

                    sub_input1 = input()

                    if re.match(r'^1', str(sub_input1)):

                        # Check the value that manager want to update
                        # Insert the new record in to the modification table
                        print("Enter the id of order you want to modified")
                        aid = str(input())
                        print("Enter the description you want to update")
                        description = str(input())
                        stmt = "UPDATE activityr\n"
                        stmt +="SET description=" + description+"\n"
                        stmt += "WHERE aid=" +aid +";"
                        query_executer(stmt)  # execute and display query and result

                    elif re.match(r'^2', str(sub_input1)):
                        print("Enter the id of order you want to modified")
                        aid = str(input())
                        stmt = "DELETE FROM activity WHERE aid="+aid+";"
                        query_executer(stmt)
                    elif re.match(r'^3', str(sub_input1)):
                        print("Enter the id of activity you want to insert")
                        aid = str(input())
                        print("Enter the description")
                        description = str(input())
                        print("Enter the mngName")
                        mngName = str(input())
                        stmt = "INSERT INTO activity " \
                               "VALUES("+aid+"," +description+","+mngName+");"
                        query_executer(stmt)

                    elif re.match(r'^4', str(sub_input1)):
                        print("Exit")
                        break
                    else:
                        print("Invalid Input")

            except Exception as e:
                print("I/O error occurred\n")
                print("ARGS:{}\n".format(e.args))
                print("Error: ", e)
                print(e.__traceback__)
                print("Context: ", e.__context__)

            
            
        

