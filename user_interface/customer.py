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

#################################################################################

### 1. Classes ### 
    
class CustomerSession(LoginSession):
    """ 
    Inherits from the LoginSession class and implements extra methods
    appropriate to Customer Functions and permissions. 
    """ 
    def __init__(self, loginsession, verbose=True): 
        """
        @args: 
            @ loginsession: an instance of the LoginSession class. Will throw an error 
            if wrong type input. 
        """
        # Initialize and typecheck
        super().__init__(verbose) # call super constructor 
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
            menu_string += "\t 3. Rate Order\n"
            menu_string += "\t 4. Pay Invoice\n"
            menu_string += "\t 5. Update preferences\n"
            menu_string += "\t 6. Exit\n"
            print(menu_string) 
            
            mgr_input = input() 
            
            if re.match(r'^1.*', str(mgr_input)): 
                self.see_mates() 
                
            elif re.match(r'^2.*', str(mgr_input)): 
                print("See my orders")
            
            elif re.match(r'^3.*', str(mgr_input)): 
                print("Rate Order")
                
            elif re.match(r'^4.*', str(mgr_input)): 
                print("Pay Invoice")
                
            elif re.match(r'^5.*', str(mgr_input)): 
                print("Update preferences")
                
            elif re.match(r'^6.*', str(mgr_input)): 
                print("Exit")
                break
            else: 
                print("Invalid Input")
                
    
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
                        break
                    
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
                        
            
    def see_orders(self): 
        """
        Display orders for the customer 
        """
        raise NotImplementedError 
        
        
    def rate_order(self): 
        """ 
        Allows the customer to rate an order. This should also be linked to 
        the function see_orders(self). 
        """
        
        
    def pay_invoice(self): 
        """
        Allows the customer to pay an invoice on an order 
        """ 
        
        raise NotImplementedError 
        
    def update_preferences(self): 
        """
        Allows the customer to update it's preferences by replacing the existing 
        ones with a new string
        """
        
        raise NotImplementedError 
        
        
        
        
        
        