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
# IMPORT DATABASE from sqlite3
# ===========================================================================

# Defining objects
conn = sqlite3.connect('walmart.sqlite')
cur = conn.cursor()

cur.execute('''SELECT sales.store_id, sales.dept_id, week.date, store.size, holidays.name, 
            markdowns.markdown, features.temperature, sales.sales
                FROM sales
                LEFT JOIN week ON sales.week_id = week.id
                LEFT JOIN store on sales.store_id = store.id
                LEFT JOIN holidays on sales.week_id = holidays.week_id
                LEFT JOIN markdowns on sales.store_id=markdowns.store_id and sales.weeknum=markdowns.weeknum
                LEFT JOIN features on sales.store_id=features.store_id and sales.week_id=features.week_id
                WHERE week.train=1''')

cols = [column[0] for column in cur.description]
df_all = pd.DataFrame.from_records(data = cur.fetchall(), columns=cols)

conn.close()



# ===========================================================================
# ADJUST DATAFRAME FOR PROPHET:
# 1. convert string to date
# 2. rename columns 
# 3. set regressors: holidays, markdown, temperature
# ===========================================================================
df_all = df_all.rename(columns={'date':'ds', 'sales':'y', 'name':'holiday'})
df_all['ds']=df_all['ds'].astype('datetime64[ns]')

flag = (df_all['store_id']==20 )&(df_all['dept_id']==92)
df = df_all[flag]

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
model.add_regressor('markdown')
model.add_regressor('temperature')
model.add_regressor('size')
model.fit(df)

future = model.make_future_dataframe(freq='w',periods=0)
future = future.merge(df[['ds','markdown','temperature','size']], how='left',left_on='ds', right_on='ds')

f1 = model.predict(future)

y_pred = f1['yhat']

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(df.ds, df.y)
ax.plot(df.ds, y_pred)

fig,(ax1,ax2)= plt.subplots(nrows=2,ncols=1,figsize=(12,8))
ax1.plot(df.ds, df.y)
ax1.plot(df.ds, df.markdown)