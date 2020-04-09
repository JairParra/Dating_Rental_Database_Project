# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 19:40:50 2020

@author: jairp
"""

#################################################################################

### 1. Imports ### 

import re
from util import query_executer
from login import LoginSession
from datetime import date

#################################################################################

### 1. Classes ### 
    
class CustomerSession(LoginSession):
    """ 
    Inherits from the LoginSession class and implements extra methods
    appropriate to Customer Functions and permissions. 
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
                
        print("CUSTOMER LOGIN: \n", self.login_resp) 
        print("CUSTOMER TYPE: \n", self.usertype)
        print("CUSTOMER VALUES: \n", self.usertype_vals)
        
        self.menu() # display appropriate options menu 
        
        
    def menu(self): 
        """
        Customized Menu with Customer Options
        """ 
        
        while True: 
            menu_string = "\n######################################################\n"
            menu_string += "                  Customer Options Menu                 \n"
            menu_string += "######################################################\n"
            menu_string += "\nPlease choose one of the available options below:\n"
            menu_string += "\t 1. See Mates\n" # will have a sub menu to see available mates --> extra menu, new order 
            menu_string += "\t 2. See my orders\n" # will have an option to : Modify order, cancel order
            menu_string += "\t 3. Pay Invoice\n"
            menu_string += "\t 4. Update preferences\n"
            menu_string += "\t 5. Exit\n"
            print(menu_string) 
            
            mgr_input = input() 
            
            if re.match(r'^1.*', str(mgr_input)): 
                self.see_mates() 
                
            elif re.match(r'^2.*', str(mgr_input)): 
                self.see_orders()
                
            elif re.match(r'^3.*', str(mgr_input)): 
                print("Pay Invoice")
                
            elif re.match(r'^4.*', str(mgr_input)): 
                self.edit_preference()
                
            elif re.match(r'^5.*', str(mgr_input)): 
                print("Exit")
                break
            else: 
                print("Invalid Input")
                
    
    def see_orders(self):
        """
        Function for menu option 2
        """

        username = self.login_resp['username']
        get_order_sql = "SELECT * FROM orderTable WHERE rid IN "
        get_order_sql += "(SELECT rid FROM request WHERE custname = '{}');".format(username)

        while True:
            query_executer(get_order_sql)
            # response_top = result.head()
            # print(response_top)
            # size = result.shape[0]
            # for i in range(size):
            #     print("{}\t{}\n".format(i,result[i]))

            print("To continue:\n")
            print("1. Make change to an order\n")
            print("2. Go back\n")
            user_input = input()

            if re.match(r'^1', str(user_input)): 
                '''to edit order'''
                self.edit_order()
            elif re.match(r'^2', str(user_input)):
                '''goes back to previous level'''
                break


    def edit_order(self):
        """
        cancel/rate an order
        """
        
        print("Please enter the order number\n")
        oid= input()

        get_order_sql = "SELECT * FROM orderTable WHERE oid = {};".format(oid)

        order_response = query_executer(get_order_sql)
        if(order_response.shape[0] == 0):
            print("Order not found\n")
        else:   
            get_request_sql = "(SELECT * FROM request WHERE rid = {});".format(order_response['rid'][0])

            request_response = query_executer(get_request_sql)

            if(request_response['custname'][0] == self.login_resp['username']):
                while True:
                    # print(request)
                    print("Would you like to\n")
                    print("1. Cancel this order\n")
                    print("2. Rate this order\n")
                    print("3. Go back\n")
                    user_input = input()
                    if re.match(r'^1', str(user_input)): 
                        '''to edit order'''
                        self.cancel_order(order_response['oid'][0])
                        print('Order cancelled')

                    elif re.match(r'^2', str(user_input)):
                        '''Rate this order'''
                        get_order_sql = "SELECT * FROM orderTable WHERE oid = {};".format(oid)

                        order_response = query_executer(get_order_sql)
                        if order_response['ordstatus'][0] != 'complete':
                            print("Cannot rate an unfinished order\n")
                            continue
                        print("From 1-5, how would you like to rate this order?\n")
                        rate = int(input())
                        if rate <=0 or rate >5:
                            print("Invalid rating\n")
                            continue 
                        self.rate_order(order_response['oid'][0], rate)
                        print("Please leave your comment.\n")
                        comment = str(input())
                        self.comment_order(order_response['oid'][0],comment)

                        date_str = self.get_current_date()
                        self.edit_rate_date(order_response['oid'][0],date_str)
                        break
                    else:
                        break
            else:
                print("Order not found\n")

    def rate_order(self, oid,rate):
        rate_order_sql = "UPDATE orderTable SET rating = {} WHERE oid = {};".format(rate,oid)
        query_executer(rate_order_sql,insert = True)
    
    def comment_order(self, oid,comment):
        comment_order_sql = "UPDATE orderTable SET comment = '{}' WHERE oid = {};".format(comment,oid)
        query_executer(comment_order_sql,insert = True)

    def cancel_order(self, oid):
        cancel_order_sql = "UPDATE orderTable SET ordStatus = 'complete' WHERE oid = {};".format(oid)
        query_executer(cancel_order_sql,insert = True)

    def edit_rate_date(self, oid, date):
        edit_sql = "UPDATE orderTable SET ratingDate = '{}' WHERE oid = {};".format(date, oid)
        query_executer(edit_sql,insert = True)

    def get_current_date(self):
        return str(date.today())

    def edit_preference(self):
        username = self.login_resp['username']
        get_customer_sql = "SELECT * FROM customer WHERE username = '{}'".format(username)

        while True:
            customer_response = query_executer(get_customer_sql)

            print('Your current preference is \n \"{}\"'.format(customer_response['preferences'][0]))
            print('please enter your new preference')
            user_input = input()

            edit_preference_sql = "UPDATE customer SET preferences = '{}' WHERE username = '{}';".format(user_input, username)
            query_executer(edit_preference_sql,insert = True)
            print("Preference editted successfully")
            break

    def see_mates(self): 
        """
        Function for menu option 1. 
        """
        
        try: 
            
            while True: 
                menu_string = "\n######################################################\n"
                menu_string += "                    Look for a Mate                   \n"
                menu_string += "######################################################\n"
                menu_string += "1. See all mates\n"
                menu_string += "2. Custom search\n" 
                menu_string += "3. Exit\n"
                print(menu_string)
                
                sub_input1 = input() 
                
                if re.match(r'^1', str(sub_input1)): 
                    
                    ## 1.7 Order by 
                    print("**Order by**")
                    print("1.Hourly Rate \n2.Age \n3.Nickname \n4.None") 
                    if re.match(r'^1', str(input())): 
                        order = "hourlyrate" 
                    elif re.match(r'^2', str(input())):
                        order = "age" 
                    elif re.match(r'^3', str(input())):
                        order = "nickname"
                    elif re.match(r'^3', str(input())):
                        order = None
                    else: 
                        print("Invalid input") 
                        continue
                    
                    stmt = "SELECT nickname,\n\t description\n\t, sex,\n\t language,\n\t height,\n\t weight,\n\t hourlyrate \n" 
                    stmt += "FROM mate m \n"
                    stmt += "JOIN usertable u \n"
                    stmt += "\t ON m.username = u.username \n"
                    if order is not None: 
                        stmt += "ORDER BY {}\n".format(order)
                    stmt += ";\n"     
                    
                    query_executer(stmt) # execute and display query and result 
                    
                elif re.match(r'^2', str(sub_input1)):
                    
                    ## 1. Custom search according to different attributes
                    print("Custom search: Choose custom preferences for your mate :) ") 
    
                    ### 1.1 Sex
                    print("Sex:\n 1) Male 2)Female") 
                    if re.match(r'^1', str(input())):
                        sex = "Male"
                    elif re.match(r'^2', str(sub_input1)): 
                        sex = "Female"
                    else: 
                        print("Invalid input") 
                        continue
                    
                    ### 1.2. Age
                    print("**Age**")
                    lower_age = input("Min: ") 
                    upper_age = input("Max: ")
                    if lower_age < 18: 
                        print("I'm calling the police...")
                        raise ValueError("WARNING: Pedophile spotted")
                    
                    ### 1.3 Languages
                    print("**Languages spoken:**")
                    print("1) English \n2) French\n3) Both")
                    if re.match(r'^1', str(input())): 
                        lang = "English" 
                    elif re.match(r'^2', str(input())):
                        lang = "French" 
                    elif re.match(r'^3', str(input())):
                        lang = "Eng & French"
                    else: 
                        print("Invalid input") 
                        continue
                    
                    ## 1.4 Height
                    print("**Height (cm)**")
                    lower_height = float(input("Min: "))/100
                    upper_height = float(input("Max: "))/100 
                    if lower_height > upper_height: 
                        print("Invalid input")
                        continue
                    
                    ## 1.5 Weight 
                    print("**Weight (kg)**")
                    lower_weight = int(input("Min: ")) 
                    upper_weight = int(input("Max: ")) 
                    if lower_weight > upper_weight: 
                        print("Invalid input")
                        continue
                    
                    ## 1.6 Hourly Rate 
                    print("**Hourly rate (CAD$)**") 
                    lower_rate = int(input("Min: "))
                    upper_rate = int(input("Max: "))
                    if lower_rate > upper_rate: 
                        print("Invalid input")
                        continue
                    
                    ## 1.7 Order by 
                    print("**Order by**")
                    print("1.Hourly Rate \n2.Age \n3.Nickname") 
                    if re.match(r'^1', str(input())): 
                        order = "hourlyrate" 
                    elif re.match(r'^2', str(input())):
                        order = "age" 
                    elif re.match(r'^3', str(input())):
                        order = "nickname"
                    else: 
                        print("Invalid input") 
                        continue
                    
                    stmt = "SELECT * FROM "
                    stmt += "\t ("
                    stmt = "\t SELECT \n"
                    stmt += "\t\t m.nickname, \n"
                    stmt += "\t\t u.sex,\n"
                    stmt += "\t\t DATE_PART('year', CURRENT_DATE) - DATE_PART('year', u.dateofbirth) AS age,\n"
                    stmt += "\t\t m.language,\n"
                    stmt += "\t\t m.height,\n"
                    stmt += "\t\t m.weight,\n" 
                    stmt += "\t\t m.hourlyrate,\n" 
                    stmt += "\t\t m.description\n"
                    stmt += "\t FROM mate m \n" 
                    stmt += "\t JOIN usertable u \n"
                    stmt += "\t\t ON m.username = u.username"
                    stmt += "\t WHERE sex='{}' AND language='{}' \n".format(sex,lang)
                    stmt += "\t\t AND (height BETWEEN {} AND {}) \n".format(lower_height, upper_height) 
                    stmt += "\t\t AND (weight BETWEEN {} AND {}) \n".format(lower_weight, upper_weight) 
                    stmt += "\t\t AND (hourlyrate BETWEEN {} AND {}) \n".format(lower_rate, upper_rate) 
                    stmt += "\t ORDER BY '{}' \n".format(order) 
                    stmt += "\t ) T"
                    stmt += "WHERE T.age BETWEEN {} AND {}".format(lower_age, upper_age)
                    stmt += ";\n" 
                    
                 
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





                        