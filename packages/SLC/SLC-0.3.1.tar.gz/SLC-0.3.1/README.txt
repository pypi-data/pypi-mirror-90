SQLite Connect (SLC) 
--------------------
SLC allows you to connect to an SQlite3 database file faster than if you just used the SQLite3 module.

Usage

- sc.run([Database_URL], [SQL_COMMAND]) # Connects to Database file and runs SQL code
- sc.run([Database_URL], [SQL_COMMAND], [argument]) # Using the new argument parameter, you can change what SLC does with the retrieved data.
- sc.RB() # Quick ROLLBACK shortcut in SQL
- sc.com() # Commit Changes
- sc.close() # Close database
- sc.cc() # Use this code to commit and close together

Argument List
- 'fetchall' --> The fetchall argument prints out the retrieved data in Python.
