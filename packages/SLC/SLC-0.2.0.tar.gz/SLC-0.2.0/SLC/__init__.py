import sqlite3

conn = ""
c = ""

def run(database_url, SQL_Command, argument):

	conn = sqlite3.connect(database_url)
	c = conn.cursor()
	if (argument.len != 0):
		if (argument == "fetchall"):
			c.execute(SQL_Command + ".fetchall()")
		else:
			print(argument + " is not a valid argument available in SLC v0.0.1")
	else:
		c.execute(SQL_Command)
    
	def com():
		conn.commit()
	def close():
		conn.close()
	def cc():
		conn.commit()
		conn.close()
	def RB():
		c.execute("ROLLBACK")
