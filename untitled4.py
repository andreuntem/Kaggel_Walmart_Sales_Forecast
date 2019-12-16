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
import numpy as np
import pandas as pd



