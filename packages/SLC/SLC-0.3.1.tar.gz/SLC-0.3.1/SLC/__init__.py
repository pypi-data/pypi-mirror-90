import sqlite3

conn = ""
c = ""

def run(database_url, SQL_Command):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute(SQL_Command)

def run_arg(database_url, SQL_Command, argument):
	
    if (argument == "fetchall"):
        conn = sqlite3.connect(database_url)
        c = conn.cursor()
        c.execute(SQL_Command)
        print(c.fetchall())
    else:
        print(argument + " is not a valid argument available in SLC v0.0.1")
    
def com():
    if (conn == ""):
        return "To use the commit function, you need to connect to a database first."
    conn.commit()
def close():
    if (conn == ""):
        return "To use the close function, you need to connect to a database first."
    conn.close()
def cc():
    if (conn == ""):
        return "To use the CC function, you need to connect to a database first."
    conn.commit()
    conn.close()
def RB():
    if (conn == ""):
        return "To use the ROLLBACK function, you need to connect to a database first."
    c.execute("ROLLBACK")
