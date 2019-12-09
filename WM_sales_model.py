"""
KAGGLE - WALMAR RECRUITING - SALES FORECAST

*** MODEL ***

https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

Questions:
    1. What are the biggest stores? (45)
    2. What are the biggest departments? (98)
    3. How many departments by store?
    4. How is it related with type of store? size or departments in store?
    5. Stores and Dept are seasonal?
    6. What is the holiday impact?
    7. Features: temperature different by store?
    #TODO : check EDA: temperature differnet by store?
    #TODO : check EDA: holiday and date same?    

Objective:
    Minimize WMAE (weighted mean absolute error),
    weight = 5 if holiday, else 1

Modelling
    # TODO: benchmark model: simplistic model: averages
    
    https://facebook.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html
    https://towardsdatascience.com/implementing-facebook-prophet-efficiently-c241305405a3
    https://mode.com/example-gallery/forecasting_prophet_python_cookbook/
    https://app.mode.com/modeanalytics/reports/d12fb67aa069/notebook
"""


# ========================================================================
# IMPORT LIBRARIES
# ========================================================================
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from fbprophet import Prophet


# ========================================================================
# DEFINING FUNCTION
# ========================================================================
def wmae(y_true,y_pred):
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    error = np.mean(abs(y_true-y_pred)/y_true)
    
    return error

# ========================================================================

def calc_dates_fwd(df):
    
    from datetime import timedelta
    from numpy import arange
    
    df_dates = pd.DataFrame(df.ds.unique())
    df_dates.rename(columns={0:'ds'},inplace=True)
    
    max_date = df_dates.max()[0].to_pydatetime()
    
    n_df_dates = len(df_dates)
    
    for i in arange(n_df_dates-1,-1,-1):
        date = df_dates.loc[i,'ds'].to_pydatetime()
        date_fwd = date + timedelta(days=+52*7)
        if date_fwd>=max_date:
            date_fwd = max_date
        df_dates.loc[i,'date_fwd'] = date_fwd
        
    return df_dates

# ========================================================================

def get_markdown(df,dates_fwd):
    
    from numpy import arange
    df = pd.merge(df,dates_fwd[['ds','date_fwd']],how='left',left_on='ds',right_on='ds')    
    df['MarkDown_c']=df['MarkDown']
    
    for i in arange(len(df)-1,-1,-1):
        markdown = df.loc[i,'MarkDown']
        
        if markdown==0:
            store = df.loc[i,'Store']
            dept = df.loc[i,'Dept']
            date_fwd = df.loc[i,'date_fwd']
            flag = (df['Store']==store)&(df['Dept']==dept)&(df['ds']==date_fwd)
            markdown = df.loc[flag,'MarkDown']
            df.loc[i,'MarkDown']=float(markdown)
                        
    return df

# ========================================================================
# IMPORT DATA and PREP
# ========================================================================

# Import Data, drop first column and change date type
df = pd.read_csv('treated_data.csv')
df.drop('Unnamed: 0',axis=1,inplace=True)
df['Date'] = df['Date'].astype('datetime64[ns]')

# Rename Columns
df.rename(columns={'Date':'ds','Weekly_Sales':'y'},inplace=True)

# Select vars
vars_sel = ['ds','Store','Dept','Size','MarkDown','y']

# Build dataframes
test = df['y'].isna()
dftr = df.loc[~test,vars_sel]
dfts = df.loc[test,vars_sel]

# Choose Store and Department sample
store_dept = (dftr['Store']==4)&(dftr['Dept']==92)
df = dftr[store_dept]
df = dftr[store_dept]

# Get holidays
holidays = pd.read_csv('holidays.csv')
holidays['date'] = holidays['date'].astype('datetime64[ns]')
holidays.rename(columns={'date':'ds'},inplace=True)

# Prepare date fwd: needed for markdown mapping
dates_fwd = calc_dates_fwd(df)

# Get markdowns
df = get_markdown(df,dates_fwd)

# ========================================================================
# TRANSFORMING VARIABLES: NORMALITY
# ========================================================================
#lamb = stats.boxcox_normmax(np.array(ys['Weekly_Sales']), brack=(-2,1.99),  method='mle')
#yt = stats.boxcox(np.array(ys['Weekly_Sales']), lamb)

#fix,(ax1,ax2) = plt.subplots(nrows=2,ncols=1,figsize=(12,8))
#stats.probplot(ys['Weekly_Sales'], dist=stats.norm, plot=ax1)
#stats.probplot(yt, dist=stats.norm, plot=ax2)

#fix,(ax1,ax2) = plt.subplots(nrows=2,ncols=1,figsize=(12,8))
#ax1.plot(ys['Weekly_Sales'])
#ax2.plot(yt)



# ========================================================================
# PREPARING DATA FOR PROPHET
# SELECTING VARIABLES
# ========================================================================
#df = ys.copy()
#df.reset_index(inplace=True)
#df['Date'] = df['Date'].astype('datetime64[ns]')
#df.rename(columns={'Date':'ds','Weekly_Sales':'y'},inplace=True)



# ========================================================================
# MODEL 1: SIMPLE ADDITIVE MODEL
# ========================================================================
m1 = Prophet(growth='linear',yearly_seasonality=5)
m1.fit(df)
future = m1.make_future_dataframe(freq='w',periods=0)
f1 = m1.predict(future)
y_pred1 = f1['yhat']
wmae_m1 = wmae(df.y,y_pred1)

# plot components
#m1.plot_components(f1)


# ========================================================================
# MODEL 2: SIMPLE MULTIPLICATIVE MODEL
# ========================================================================
m2 = Prophet(growth='linear', seasonality_mode='multiplicative',yearly_seasonality=5)
m2.fit(df)
future = m2.make_future_dataframe(freq='w',periods=0)
f2 = m2.predict(future)
y_pred2 = f2['yhat']
wmae_m2 = wmae(df.y,y_pred2)

# plot components
#m2.plot_components(f2)



# ========================================================================
# MODEL 3: MULTIPLICATIVE MODEL SEASONALITY
# ========================================================================

m3 = Prophet(growth='linear',
             seasonality_mode='multiplicative',
             holidays=holidays,
             daily_seasonality=False,
             weekly_seasonality=False,
             yearly_seasonality=False,
             ).add_seasonality(
                     name='52wk',
                     period=365.25,
                     fourier_order=10)
m3.fit(df)
future = m3.make_future_dataframe(freq='w',periods=0)
f3 = m3.predict(future)
y_pred3 = f3['yhat']
wmae_m3 = wmae(df.y,y_pred3)

# plto components
#m3.plot_components(f3)

# ========================================================================
# MODEL 4: MULTIPLICATIVE MODEL SEASONALITY + MARKDOWN
# ========================================================================

m4 = Prophet(growth='linear',
             seasonality_mode='multiplicative',
             holidays=holidays,
             daily_seasonality=False,
             weekly_seasonality=False,
             yearly_seasonality=False,
             ).add_seasonality(
                     name='52wk',
                     period=365,
                     fourier_order=10)
m4.add_regressor('MarkDown')
m4.fit(df)
future = m4.make_future_dataframe(freq='w',periods=0)
future = pd.merge(future,df[['ds','MarkDown']],how='left',left_on='ds',right_on='ds')
f4 = m4.predict(future)
y_pred4 = f4['yhat']
wmae_m4 = wmae(df.y,y_pred4)

# plot components
m4.plot_components(f4)



# ========================================================================
# MODEL 4: MULTIPLICATIVE MODEL SEASONALITY + MARKDOWN
# ========================================================================
# plot actuals vs forecast
fig, (ax1,ax2,ax3,ax4) = plt.subplots(ncols=1,nrows=4,figsize=(15,10))
ax1.plot(df.ds,df.y)
ax1.plot(df.ds,y_pred1)
ax2.plot(df.ds,df.y)
ax2.plot(df.ds,y_pred2)
ax3.plot(df.ds,df.y)
ax3.plot(df.ds,y_pred3)
ax4.plot(df.ds,df.y)
ax4.plot(df.ds,y_pred4)
ax1.set_title('1: SIMPLE ADDITIVE: {:.4f}'.format(wmae_m1))
ax2.set_title('2: SIMPLE MULTIPLICATIVE: {:.4f}'.format(wmae_m2))
ax3.set_title('3: SEASONAL MULT: {:.4f}'.format(wmae_m3))
ax4.set_title('4: SEASONAL MULT + MARKDOWN: {:.4f}'.format(wmae_m4))
ax1.set_xticks([])
ax2.set_xticks([])
ax3.set_xticks([])


print('final')
