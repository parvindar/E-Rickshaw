import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

# drop table if exists stand ;
# create table stand (
#   i integer primary key autoincrement,
#   standid text,
#   name text,
#   x float,
#   y float,
#   requests text
# );

# drop table if exists user ;
# create table user(
# 	id integer primary key autoincrement,
# 	cardid text,
# 	name text,
# 	email text,
# 	phone text,
# 	balance float

# SQLite DB Table Schema
TableSchema="""
drop table if exists rickshaw ;
create table rickshaw (
  id integer primary key autoincrement,
  name text,
  email text,
  ricknum text,
  phone integer,
  pass text
);

drop table if exists rickshaw_active ;
create table rickshaw_active (
  i integer primary key autoincrement,
  id text,
  name text,
  x float,
  y float,
  phone text,
  ricknum text,
  passengers integer,
  active bit);

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