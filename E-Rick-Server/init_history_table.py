import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists history ;
create table history (
  id integer primary key autoincrement,
  time integer,
  source text,
  destination text,
  rickid text,
  passenger text,
  card text,
  cost float
);

"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
conn.commit()
curs.close()
conn.close()