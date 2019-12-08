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
"""


# ========================================================================
# IMPORT LIBRARIES
# ========================================================================
import numpy as np
import pandas as pd


# ========================================================================
# IMPORT DATA and PREP
# ========================================================================
df   = pd.read_csv('treated_data.csv')
test = df['Weekly_Sales'].isna()
X    = df[~test].drop('Weekly_Sales',axis=1)
Xt   = df[test].drop('Weekly_Sales',axis=1)
y    = df.loc[~test,'Weekly_Sales']


# ========================================================================
# CREATE MODEL SARIMAX
# ========================================================================


print('final')
