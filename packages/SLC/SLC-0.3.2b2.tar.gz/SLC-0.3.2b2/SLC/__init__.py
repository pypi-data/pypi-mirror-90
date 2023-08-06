import sqlite3

conn = None
c = None


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
    elif (argument == "cc"):
        conn = sqlite3.connect(database_url)
        c = conn.cursor()
        c.execute(SQL_Command)
        conn.commit()
        conn.close()
    elif (argument == "com"):
        conn = sqlite3.connect(database_url)
        c = conn.cursor()
        c.execute(SQL_Command)
        c.commit()
    elif (argument == "close"):
        conn = sqlite3.connect(database_url)
        c = conn.cursor()
        c.execute(SQL_Command)
        conn.close()
    elif (argument == "RB"):
        conn = sqlite3.connect(database_url)
        c = conn.cursor()
        c.execute(SQL_Command)
        c.execute("ROLLBACK")
    else:
        print(argument + " is not a valid argument available in SLC v0.3.2")

def run_args2(database_url, SQL_Command, argument1, argument2):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute(SQL_Command)
    if (argument1 == "fetchall"):
        print(c.fetchall())
    elif (argument1 == "cc"):
        conn.commit()
        conn.close()
    elif (argument1 == "com"):
        conn.commit()
    elif (argument1 == "close"):
        conn.close()
    elif (argument1 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument1 + " is not a valid argument available in SLC v0.3.2")
    if (argument2 == "fetchall"):
        print(c.fetchall())
    elif (argument2 == "cc"):
        conn.commit()
        conn.close()
    elif (argument2 == "com"):
        conn.commit()
    elif (argument2 == "close"):
        conn.close()
    elif (argument2 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument2 + " is not a valid argument available in SLC v0.3.2")

def run_args3(database_url, SQL_Command, argument1, argument2, argument3):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute(SQL_Command)
    if (argument1 == "fetchall"):
        print(c.fetchall())
    elif (argument1 == "cc"):
        conn.commit()
        conn.close()
    elif (argument1 == "com"):
        conn.commit()
    elif (argument1 == "close"):
        conn.close()
    elif (argument1 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument1 + " is not a valid argument available in SLC v0.3.2")
    if (argument2 == "fetchall"):
        print(c.fetchall())
    elif (argument2 == "cc"):
        conn.commit()
        conn.close()
    elif (argument2 == "com"):
        conn.commit()
    elif (argument2 == "close"):
        conn.close()
    elif (argument2 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument2 + " is not a valid argument available in SLC v0.3.2")
    if (argument3 == "fetchall"):
        print(c.fetchall())
    elif (argument3 == "cc"):
        conn.commit()
        conn.close()
    elif (argument3 == "com"):
        conn.commit()
    elif (argument3 == "close"):
        conn.close()
    elif (argument3 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument3 + " is not a valid argument available in SLC v0.3.2")
def run_args4(database_url, SQL_Command, argument1, argument2, argument3, argument4):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute(SQL_Command)
    if (argument1 == "fetchall"):
        print(c.fetchall())
    elif (argument1 == "cc"):
        conn.commit()
        conn.close()
    elif (argument1 == "com"):
        conn.commit()
    elif (argument1 == "close"):
        conn.close()
    elif (argument1 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument1 + " is not a valid argument available in SLC v0.3.2")
    if (argument2 == "fetchall"):
        print(c.fetchall())
    elif (argument2 == "cc"):
        conn.commit()
        conn.close()
    elif (argument2 == "com"):
        conn.commit()
    elif (argument2 == "close"):
        conn.close()
    elif (argument2 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument2 + " is not a valid argument available in SLC v0.3.2")
    if (argument3 == "fetchall"):
        print(c.fetchall())
    elif (argument3 == "cc"):
        conn.commit()
        conn.close()
    elif (argument3 == "com"):
        conn.commit()
    elif (argument3 == "close"):
        conn.close()
    elif (argument3 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument3 + " is not a valid argument available in SLC v0.3.2")
    if (argument4 == "fetchall"):
        print(c.fetchall())
    elif (argument4 == "cc"):
        conn.commit()
        conn.close()
    elif (argument4 == "com"):
        conn.commit()
    elif (argument4 == "close"):
        conn.close()
    elif (argument4 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument4 + " is not a valid argument available in SLC v0.3.2")
def run_args5(database_url, SQL_Command, argument1, argument2, argument3, argument4, argument5):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute(SQL_Command)
    if (argument1 == "fetchall"):
        print(c.fetchall())
    elif (argument1 == "cc"):
        conn.commit()
        conn.close()
    elif (argument1 == "com"):
        conn.commit()
    elif (argument1 == "close"):
        conn.close()
    elif (argument1 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument1 + " is not a valid argument available in SLC v0.3.2")
    if (argument2 == "fetchall"):
        print(c.fetchall())
    elif (argument2 == "cc"):
        conn.commit()
        conn.close()
    elif (argument2 == "com"):
        conn.commit()
    elif (argument2 == "close"):
        conn.close()
    elif (argument2 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument2 + " is not a valid argument available in SLC v0.3.2")
    if (argument3 == "fetchall"):
        print(c.fetchall())
    elif (argument3 == "cc"):
        conn.commit()
        conn.close()
    elif (argument3 == "com"):
        conn.commit()
    elif (argument3 == "close"):
        conn.close()
    elif (argument3 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument3 + " is not a valid argument available in SLC v0.3.2")
    if (argument4 == "fetchall"):
        print(c.fetchall())
    elif (argument4 == "cc"):
        conn.commit()
        conn.close()
    elif (argument4 == "com"):
        conn.commit()
    elif (argument4 == "close"):
        conn.close()
    elif (argument4 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument4 + " is not a valid argument available in SLC v0.3.2")
    if (argument5 == "fetchall"):
        print(c.fetchall())
    elif (argument5 == "cc"):
        conn.commit()
        conn.close()
    elif (argument5 == "com"):
        conn.commit()
    elif (argument5 == "close"):
        conn.close()
    elif (argument5 == "RB"):
        c.execute("ROLLBACK")
    else:
        print(argument5 + " is not a valid argument available in SLC v0.3.2")
    
def com():
    return "The SLC.com() function has been deprecated. Due to multiple issues concerning database protection and safety. Please use the run_arg, or run_args[number] to use the argument."

def close():
    return "The SLC.close() function has been deprecated. Due to multiple issues concerning database protection and safety. Please use the run_arg, or run_args[number] to use the argument."

def cc():
    return "The SLC.cc() function has been deprecated. Due to multiple issues concerning database protection and safety. Please use the run_arg, or run_args[number] to use the argument."

def RB():
    return "The SLC.RB() function has been deprecated. Due to multiple issues concerning database protection and malfunctioning databases. Please use the run_arg, or run_args[number] to use the argument."