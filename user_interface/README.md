# user_interface 
- Code for the implentation of a friendly user interface. **Currently implemented as I/O**, but may migrate to actual front-end in the future. 

## Descripion of main scripts

### main.py

- `main.py`: Driver script; manages main menu and command-line argument options (not implemented), including log-in propmts for users and administrator, delivering the proper acess. 

### login.py
- `login.py`: Contains the parent class `LoginSession()`, which implements the following methods: 
  - `__init__(self, newuser = {}, verbose=True)` : Constructor, is `newuser==True`, the constructor will call `LoginSession().newuser()`, which will initialize a procedure to create and store a new user in the database. 
  - `newuser(self)`: User-interactive procedure to create and insert a new user of type *Customer* or *Mate* into the database. 
  - `login(self, user="", password="", verbose=True)` : Validates user log-in credentials in the database, and returns a dictionary object containing a value `login_resp['login_status'] == True` if login was successful and `False`otherwise. If login was successful, response with all the values for matched user record are returned. If no user existed, response object will be `None`. 
  - `fetch_usertype`: Determines usertype and fetches all the corresponding values from the appropriate derived table if `fetch_all==True`. 
  
  #### Example usage: 
  ```Python
    # fetch username 
    user = input("Username or email: ") 
    password = getpass() # obtain screen encrypted password
    logses = LoginSession() # instantiate object
    login = logses.login(user=user, password=password) # this will return all login info
    
    # If login was successful
    if login['login_status'] == True: 
        print("Successful login!")
        print("Login response: \n", login, "\n")
        logses.fetch_usertype() # retrieve values for usertype
        print("Usertype values: \n", logses.usertype_vals)  
  ```

### customer.py 
- `customer.py`: Contains a child class `CustomerSession(LoginSession)` inheriting from `login.LoginSession()`. This class implements options related to *Customer* , with the appropriate permissions. 
  - `__init__(self, loginsession, verbose=True)`: Overriding constructor. The `loginsession` argument allows to copy existent values from an already isntantiated `LoginSession()` object. 
  - `menu(self)`: Main menu for *Customer*
  - `see_mates(self)`: Provides a sub-menu with an option to display (non-sensible) information of all mates, or allows a custom search of mates. 
  
### manager.py 
- `manager.py`: Contains the child class `ManagerSession(LoginSession)` inheriting from `login.LoginSession()`.This class implements options related to *Customer* , with the appropriate permissions. 
  - `menu(self)`: Main menu for *Manager* 
  
### mate.py
- `manager.py`: Contains the child class `MateSession(LoginSession)` inheriting from `login.LoginSession()`.This class implements options related to *Customer* , with the appropriate permissions. 
  - `menu(self)`: Main menu for *Mater*

### admin.py 
- `manager.py`: Contains the child class `MateSession(LoginSession)` inheriting from `login.LoginSession()`.This class implements options related to *Customer* , with the appropriate permissions. 
  - `menu(self)`: Main menu for an administrator. 
  - `master_query(self)`: Prompts a custom SQL query and attempts to execute it in the datase. 
  
### Other scripts and files
  
### util.py 
- `util.py`: Script containing helper functions. 
  - `config(filename='database.ini', section='postgresql')`: Provides configurations for database access. the text file `database.ini` must exist under the same directory, and contains database connection parameters. 
  - `query_executer(stmt, verbose=True)`: Accepts a SQL statement as an input, assumed to be correct and end by a semi-colon. If `verbose==True`, it will display the input query along with the output. **returns** a Pandas dataframe with the output query along with the approprite columns. 
  
### connection_example.py 
- `connection_example.py`: Contains an example script showing how to connect to, execute queries in the database and fetch the results.

### database.ini 
- Text file containing database configuration parameters. 
