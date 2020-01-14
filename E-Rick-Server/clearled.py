import sqlite3

DB_Name = 'IoT.db'
TableSchema="update stand set requests = '[0, 0, 0, 0, 0, 0, 0, 0]'"


#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
#sqlite3.complete_statement(TableSchema)
curs.execute(TableSchema)
#Close DB
conn.commit()
curs.close()
conn.close()

