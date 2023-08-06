# Shortcuts
def dropDB(database_url):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute("DROP DATABASE " + database_url)
def dropTB(database_url, table):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute("DROP TABLE " + table)
def bkDB(database_url, disk_filepath):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute("BACKUP DATABASE " + database_url)
    c.execute("TO DISK = '" + disk_filepath + "\'")
def cT(database_url, table_name, attr):
    conn = sqlite3.connect(database_url)
    c = conn.cursor()
    c.execute("CREATE TABLE " + table_name + "(" + attr + ")")