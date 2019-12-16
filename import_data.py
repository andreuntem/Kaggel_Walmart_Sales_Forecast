# -*- coding: utf-8 -*-
"""
KAGGLE - WALMART SALES FORECAST

[1] DATA PREPARATION: CREATE SQL DATABASE

@author: Andre
"""



# ===========================================================================
# IMPORT LIBRARIES
# ===========================================================================
import sqlite3
import csv


# ===========================================================================
# CREATE SQL DATABASE:
# sales: (week_id, stores_id, dept_id), sales
# week: (id, date), holiday, train
# stores: (id, store_id), size, type
# dept: (id, dept_id))
# features: (id, store_id, date_id), temp, fuel, cpi, ...
# ===========================================================================

conn = sqlite3.connect('walmart.sqlite')
cur = conn.cursor()

# Table: week
cur.execute('DROP TABLE IF EXISTS week')
cur.execute('CREATE TABLE week (id INTEGER PRIMARY KEY, date TEXT UNIQUE, train INTEGER)')

# Table: store
cur.execute('DROP TABLE IF EXISTS store')
cur.execute('CREATE TABLE store (id INTEGER PRIMARY KEY, name TEXT UNIQUE, size REAL, type TEXT)')

# Table: dept
cur.execute('DROP TABLE IF EXISTS dept')
cur.execute('CREATE TABLE dept (id INTEGER PRIMARY KEY, name TEXT UNIQUE)')

# Table: sales
cur.execute('DROP TABLE IF EXISTS sales')
cur.execute('''CREATE TABLE sales 
            (store_id INTEGER, dept_id INTEGER, week_id TEXT, sales REAL, 
            UNIQUE(store_id, dept_id, week_id))''')

# Table: holidays
cur.execute('DROP TABLE IF EXISTS holidays')
cur.execute('CREATE TABLE holidays (id INTEGER PRIMARY KEY, date TEXT UNIQUE, name TEXT)')

# Table: features
#cur.execute('DROP TABLE IF EXISTS features')
#cur.execute('CREATE TABLE features (id INTEGER PRIMARY KEY,  TEXT, size INTEGER, type TEXT)')


# ===========================================================================
# READ TRAINING.CSV
# Populate: week, store, dept and sales
# ===========================================================================

with open('train.csv','r') as csvfile:


    csvreader = csv.reader(csvfile)    
    next(csvreader)
    
    for row in csvreader:
        
        store_i = row[0]
        dept_i  = row[1]
        date_i  = row[2]
        sales_i = row[3]
        isholiday_i = row[4]
        
        # Populate: week
        try:
            cur.execute('INSERT OR IGNORE INTO week (date,train) VALUES (?,?)',(date_i,1,))
        except:
            pass
    

        # Populate: store
        try:
            cur.execute('INSERT OR IGNORE INTO store (name) VALUES (?)',(store_i,))
        except:
            pass


        # Populate: dept
        try:
            cur.execute('INSERT OR IGNORE INTO dept (name) VALUES (?)',(dept_i,))
        except:
            pass


        # Populate: sales
        try:
            cur.execute('INSERT OR IGNORE INTO sales (store_id,dept_id,week_id,sales) VALUES (?,?,?,?)',(store_i,dept_i,date_i,sales_i,))
        except:
            pass

conn.commit()


# ===========================================================================
# READ TEST.CSV
# Populate: week, store, dept and sales
# ===========================================================================

with open('test.csv','r') as csvfile:


    csvreader = csv.reader(csvfile)    
    next(csvreader)
    
    for row in csvreader:
        
        store_i = row[0]
        dept_i  = row[1]
        date_i  = row[2]
        #sales_i = row[3]
        isholiday_i = row[3]
        
        # Populate: week
        try:
            cur.execute('INSERT OR IGNORE INTO week (date,train) VALUES (?,?)',(date_i,0,))
        except:
            pass
    

        # Populate: store
        try:
            cur.execute('INSERT OR IGNORE INTO store (name) VALUES (?)',(store_i,))
        except:
            pass


        # Populate: dept
        try:
            cur.execute('INSERT OR IGNORE INTO dept (name) VALUES (?)',(dept_i,))
        except:
            pass


        # Populate: sales
        try:
            cur.execute('INSERT OR IGNORE INTO sales (store_id,dept_id,week_id,sales) VALUES (?,?,?,?)',(store_i,dept_i,date_i,None,))
        except:
            pass

conn.commit()


# ===========================================================================
# READ HOLIDAY.CSV
# Populate: week, store, dept and sales
# cur.execute('CREATE TABLE holidays (id INTEGER PRIMARY KEY, date TEXT UNIQUE, name TEXT)')
# ===========================================================================

with open('holidays.csv','r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    next(csvreader)
    
    for row in csvreader:
        date_i = row[0]
        holiday_i = row[1]
        
        
        try:
            cur.execute('INSERT OR IGNORE INTO holidays (date, name) VALUES (?,?)',(date_i,holiday_i))
        except:
            pass
        
conn.commit()


# ===========================================================================
# READ STORES.CSV
# Populate: week, store, dept and sales
# ===========================================================================
            
with open('stores.csv','r') as csvfile:

    csvreader = csv.reader(csvfile)    
    next(csvreader)
    
    for row in csvreader:
        
        store_i = row[0]
        type_i  = row[1]
        size_i  = row[2]
        
        # Populate: week
        try:
            cur.execute('''UPDATE store 
                        SET size = ?,type=? 
                        WHERE name= ? ''', (size_i,type_i,store_i))
        except:
            pass

conn.commit()





conn.close()
