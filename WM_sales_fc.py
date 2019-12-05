"""
KAGGLE - WALMAR RECRUITING - SALES FORECAST
https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

Questions:
    1. What are the biggest stores? (45)
    2. What are the biggest departments? (98)
    3. How many departments by store?
    4. How is it related with type of store? size or departments in store?
    5. Stores and Dept are seasonal?
    6. What is the holiday impact?

Objective:
    Minimize WMAE (weighted mean absolute error),
    weight = 5 if holiday, else 1
"""


# ========================================================================
# IMPORT LIBRARIES
# ========================================================================
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns



# ========================================================================
# IMPORT DATA
# ========================================================================
df = pd.read_csv('train.csv')
df['Date_str']=df['Date'].apply(lambda x: str(x))

stores = pd.read_csv('stores.csv')

sns.jointplot('Type','Size',data=stores)
plt.show()

pvt = pd.pivot_table(df,index='Store',values='Weekly_Sales')
pvt = pvt.reset_index()



print('final')
