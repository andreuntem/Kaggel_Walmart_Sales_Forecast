# -*- coding: utf-8 -*-
"""
KAGGLE - WALMART SALES FORECAST

<<< CREATE SQL DATABASE >>>

week: (id), date, train
dept: (id), name
stores: (id), name, size, type
sales: (week_id, dept_id, stores_id), sales
features: (store_id, week_id), temperature, fuel, mkd1-5, cpi, unemployment
holidays (week_id), holiday

"""



# ===========================================================================
# IMPORT LIBRARIES
# ===========================================================================
import sqlite3
import csv


# ===========================================================================
# CREATE SQL DATABASE and TABLES
# ===========================================================================

conn = sqlite3.connect('walmart.sqlite')
cur = conn.cursor()

# Table: week
cur.execute('DROP TABLE IF EXISTS week')
cur.execute('CREATE TABLE week (id INTEGER PRIMARY KEY, date TEXT UNIQUE, train INTEGER)')

# Table: dept
cur.execute('DROP TABLE IF EXISTS dept')
cur.execute('CREATE TABLE dept (id INTEGER PRIMARY KEY, name TEXT UNIQUE)')

# Table: store
cur.execute('DROP TABLE IF EXISTS store')
cur.execute('CREATE TABLE store (id INTEGER PRIMARY KEY, name TEXT UNIQUE, size REAL, type TEXT)')

# Table: sales
cur.execute('DROP TABLE IF EXISTS sales')
cur.execute('''CREATE TABLE sales 
            (store_id INTEGER, dept_id INTEGER, week_id TEXT, sales REAL, 
            UNIQUE(store_id, dept_id, week_id))''')

# Table: holidays
cur.execute('DROP TABLE IF EXISTS holidays')
cur.execute('CREATE TABLE holidays (week_id INTEGER UNIQUE, name TEXT)')

# Table: features
cur.execute('DROP TABLE IF EXISTS features')
cur.execute('''CREATE TABLE features (store_id INTEGER, week_id INTEGER, temperature REAL,
                                      fuel REAL, markdown1 REAL, markdown2 REAL,
                                      markdown3 REAL, markdown4 REAL,
                                      markdown5 REAL, markdown REAL,
                                      cpi REAL, unemployment REAL,
                                      UNIQUE (store_id, week_id))''')


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

        # Populate: dept
        try:
            cur.execute('INSERT OR IGNORE INTO dept (name) VALUES (?)',(dept_i,))
        except:
            pass

        # Populate: store
        try:
            cur.execute('INSERT OR IGNORE INTO store (name) VALUES (?)',(store_i,))
        except:
            pass

        # Populate: sales
        try:
            cur.execute('SELECT id FROM week WHERE date = ?',(date_i,))
            ii = cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO sales (store_id,dept_id,week_id,sales) 
            VALUES (?,?,?,?)''',(store_i,dept_i,ii,sales_i,))
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
        isholiday_i = row[3]
        
        # Populate: week
        try:
            cur.execute('INSERT OR IGNORE INTO week (date,train) VALUES (?,?)',(date_i,0,))
        except:
            pass
    
        # Populate: dept
        try:
            cur.execute('INSERT OR IGNORE INTO dept (name) VALUES (?)',(dept_i,))
        except:
            pass
        
        # Populate: store
        try:
            cur.execute('INSERT OR IGNORE INTO store (name) VALUES (?)',(store_i,))
        except:
            pass

        # Populate: sales
        try:
            cur.execute('SELECT id FROM week WHERE date = ?',(date_i,))
            ii = cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO sales (store_id,dept_id,week_id,sales) 
            VALUES (?,?,?,?)''',(store_i,dept_i,ii,None,))
        except:
            pass

conn.commit()


# ===========================================================================
# READ HOLIDAY.CSV
# Populate: week_id, holiday
# ===========================================================================

with open('holidays.csv','r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    next(csvreader)
    
    for row in csvreader:
        date_i = row[0]
        holiday_i = row[1]
        
        cur.execute('SELECT id FROM week WHERE date = ?',(date_i,))
        try:
            ii = cur.fetchone()[0]
            cur.execute('INSERT OR IGNORE INTO holidays (week_id, name) VALUES (?,?)',(ii,holiday_i))
        except:
            pass
        
conn.commit()


# ===========================================================================
# READ STORES.CSV
# Populate: stores size and type
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

# ===========================================================================
# READ FEATURES.CSV
# Populate: stores size and type
# ===========================================================================

with open('features.csv','r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    next(csvreader)
    
    for row in csvreader:
        store_i = row[0]
        date_i  = row[1]
        temp_i  = row[2]
        fuel_i  = row[3]
        mkd1_i  = 0 if row[4]=='NA' else row[4]
        mkd2_i  = 0 if row[5]=='NA' else row[5]
        mkd3_i  = 0 if row[6]=='NA' else row[6]
        mkd4_i  = 0 if row[7]=='NA' else row[7]
        mkd5_i  = 0 if row[8]=='NA' else row[8]
        mkd_i = float(mkd1_i) + float(mkd2_i) + float(mkd3_i) + float(mkd4_i) + float(mkd5_i)
        cpi_i   = row[9]
        unemp_i = row[10]
        
        try:
            # Find store_id
            cur.execute('SELECT id FROM store WHERE name = ?',(store_i,))
            store_id = cur.fetchone()[0]
            
            # Find week_id
            cur.execute('SELECT id FROM week WHERE date = ?',(date_i,))
            week_id = cur.fetchone()[0]
            
            # Populate feature table:
            cur.execute('''INSERT OR IGNORE INTO features(store_id, week_id, temperature,
                                                        fuel,markdown1,markdown2,markdown3,
                                                        markdown4,markdown5,
                                                        markdown,cpi,unemployment)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (store_id, week_id, temp_i,fuel_i,mkd1_i,mkd2_i,mkd3_i,mkd4_i,mkd5_i,
                 mkd_i,cpi_i,unemp_i))
            
        except:
            pass

conn.commit()


# ===========================================================================
# COMPLETE FEATURES.MARKDOWN
# ===========================================================================



conn.close()



# ===========================================================================
# TEST:: QUERY
# ===========================================================================
        
#conn = sqlite3.connect('walmart.sqlite')
#cur = conn.cursor()
#cur.execute('SELECT * FROM holidays')
#import pandas as pd
#cols = [column[0] for column in cur.description]
#results = pd.DataFrame.from_records(data = cur.fetchall(), columns=cols)
#conn.close()