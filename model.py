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
import pandas as pd

import matplotlib.pyplot as plt

from fbprophet import Prophet


# ===========================================================================
# DEFINING FUNCTIONS
# ===========================================================================

    
    


# ===========================================================================
# IMPORT DATABASE
# from sqlite3
# https://www.sqlitetutorial.net/sqlite-inner-join/
# ===========================================================================

# Defining objects
conn = sqlite3.connect('walmart.sqlite')
cur = conn.cursor()

store = 20
dept  = 92
cur.execute('''SELECT
            sales.store_id, sales.dept_id, 
            sales.sales as y,
            week.date as ds,
            store.size as store_size,
            holidays.name as holiday,
            features.temperature as temp
            FROM sales
            LEFT JOIN store ON sales.store_id = store.id
            LEFT JOIN week ON sales.week_id = week.id
            LEFT JOIN holidays ON holidays.week_id = week.id
            LEFT JOIN features ON features.store_id = store.id AND features.week_id = week.id            
            WHERE week.train=1 AND sales.store_id= ? AND sales.dept_id = ?
            ORDER BY week.date ASC''',
            (store, dept, ))

cols = [column[0] for column in cur.description]
df = pd.DataFrame.from_records(data = cur.fetchall(), columns=cols)

conn.close()


# ===========================================================================
# MODEL
# ===========================================================================
model = Prophet(growth='linear',
                seasonality_mode='multiplicative',
                daily_seasonality=False,
                weekly_seasonality=False,
                yearly_seasonality=False,
                ).add_seasonality(
                        name='52wks',
                        period=365,
                        fourier_order=10)

model.fit(df)
future = model.make_future_dataframe(freq='w',periods=0)
f1 = model.predict(future)
y_pred = f1['yhat']

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(df.ds, df.y)
ax.plot(df.ds, y_pred)
