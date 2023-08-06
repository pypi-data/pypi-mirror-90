# SQLite Connect (SLC) 

SLC allows you to connect to an SQLite3 database file faster than if you just used the SQLite3 module. Connect to a database, write to it, and commit and close it all in one line.

## Usage
- Individual argument functions won't be supported in this version because of easy mistakes and unsupported Python issues.
```python
SLC.run([Database_URL], [SQL_COMMAND]) # Connects to Database file and runs SQL code
```
```python
SLC.run_arg([Database_URL], [SQL_COMMAND], [argument]) # Adds one new argument parameter over the original run command.
```
```python
SLC.run_args2([Database_URL], [SQL_COMMAND], [argument1], [argument2]) # Lets you input 2 arguments into run function.
```
```python
SLC.run_args3([Database_URL], [SQL_COMMAND], [argument1], [argument2], [argument3]) # Lets you input 3 arguments into run function.
```
```python
SLC.run_args4([Database_URL], [SQL_COMMAND], [argument1], [argument2], [argument3], [argument4]) # Lets you input 4 arguments into run function.
```
```python
SLC.run_args5([Database_URL], [SQL_COMMAND], [argument1], [argument2], [argument3], [argument4], [argument5]) # Lets you input 5 arguments into run function.
```

## Argument List

- 'fetchall' --> The fetchall argument prints out the retrieved data in Python.
- 'cc' --> CC will commit and close the SQLite3 file after the SQL command is run.
- 'com' --> This will only commit the file automatically after running SQL command.
- 'close' --> Will only close the SQLite3 file after SQL command is done running.
- 'RB' --> Will automatically rollback any SQL command you just ran. IDK why you would need this, but I added it anyway, so it would keep it consistent (and look like I have a lot of args).
