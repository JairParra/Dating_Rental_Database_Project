# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:06:02 2020

@author: jairp
"""

################################################################################

### 1. Imports 

import os
import re
import sys
import time
import useroptions 
import argparse 
import pandas as pd

###############################################################################

### 2. Application arguments setup 

description = """Application to interact with the mate rental database.
                Please choose one of the options displayed."""

parser = argparse.ArgumentParser(description=description) 
parser.add_argument("--option",help="Run input command number")
parser.add_argument("--arg1", help="Argument 1") # argument accepting input path 
parser.add_argument("--boolarg1",help="Boolean argument, stores boolean", 
                    action="store_true")
parser.add_argument("--verbose", help="Display more information")
parser.add_argument("--demo", help="Run a demo")
args = parser.parse_args() # obtain arguments 

###############################################################################

### 3. Driver script

if __name__ == '__main__': 
    
    # Options pased as arguments by command line 
    if args.option: 
        print("Chosen option = ", args.option)
    if args.demo: 
        print("Running demo...")
    
    ## Main Loop 
    while True: 
        
        # Menu display 
        options_string = "Welcome to the MateRental database! \n"
        options_string += "Please choose one of the available options below:\n"
        options_string += "\t 1. Option1\n" 
        options_string += "\t 2. Option2\n" 
        options_string += "\t 3. Option3\n" 
        options_string += "\t 4. Option4\n" 
        options_string += "\t 5. Option5\n" 
        options_string += "\t 6. Quit\n" 
        print(options_string) 
        
        if args.demo: 
            print("Running demo...")
        
        # Obtain user options
        try: 
            # Prompt and parse input
            print("Please select an option by selecting a number")
            user_input = input() 
            print("Your input: ", user_input) 
            
            if re.match(r'^6.*', str(user_input)): 
                print("Good bye! :) ")
                sys.exit() 
                break 
            
        except Exception as e: 
            print("I/O error occurred\n")
            print("ARGS:{}\n".format(e.args))
            e.with_traceback() # output traceback 







