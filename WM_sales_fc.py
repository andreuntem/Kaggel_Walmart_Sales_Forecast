"""
KAGGLE - WALMAR RECRUITING - SALES FORECAST
https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

Questions:
    1. What are the biggest stores?
    2. What are the biggest departments?
    3. Stores and Dept are seasonal?
    4. What is the holiday impact?
    5. 
"""

# ========================================================================
# IMPORT LIBRARIES
# ========================================================================
import numpy as np
import pandas as pd


# ========================================================================
# IMPORT DATA
# ========================================================================
df = pd.read_csv('train.csv')
df['Date_str']=df['Date'].apply(lambda x: str(x))

stores = pd.read_csv('stores.csv')





print('final')
