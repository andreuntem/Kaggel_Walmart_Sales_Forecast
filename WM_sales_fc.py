"""
KAGGLE - WALMAR RECRUITING - SALES FORECAST
https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

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


stores = pd.read_csv('stores.csv')
print(stores.head(10))




print('final')
