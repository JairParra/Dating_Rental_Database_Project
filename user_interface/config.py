#!/usr/bin/python 

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:30:31 2020

config.py 

Configuration file for connection with Postgres database (remote) 
"""

from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'): 
    """
    Provides configurations for database access
    """
    
    # create a parser 
    parser = ConfigParser() 
    # read config file 
    parser.read(filename) 
    
    # get section, default to postgresql 
    db = {} 
    if parser.has_section(section): 
        params = parser.items(section) # obtain parameters 
        for param in params: 
            db[param[0]] = param[1] # assign params to database 
    else:
        raise Exception("Section {0} not found in the {1} file".format(section, filename)) 
        
    # return the database object 
    return db 
            

