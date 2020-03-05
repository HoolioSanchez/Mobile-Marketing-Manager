#%%
from dataManager import DataManager
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import theseus_growth as th 

#%%
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import scipy.interpolate 
#%%
dm = DataManager()
th = th.theseus()

#%%
# ad_rev = dm.ironsourceDataFrame('2019-12-01','2019-12-31')
#%%
# ad_rev['date'] = pd.to_datetime(ad_rev['date'])
# ad_rev.set_index('date', inplace=True)
# panda = ad_rev[ad_rev['appName'].str.contains('Panda')]
# pp_rev = panda['revenue'].resample('d').sum()
# pp_rev = pp_rev.reset_index()
# pp_rev = pp_rev.drop('date', axis = 1)
# pp_rev.head()
# #%%
# dau = dm.dailyActiveUserDataframe('dau_data')
# dau.head()

# #%%
# pp_rev['arpdau'] = pp_rev['revenue'] / dau['DAU']
# #%%
# pp_rev.head()
# #%%
# pp_rev.to_csv('adrev.csv')
#%%
reten = dm.retentionDataFrame('retention_data')
reten.set_index('install_dt', inplace = True)
reten.index = pd.to_datetime(reten.index)
reten = dm.calculateRetentionPct(reten)
reten.head()

#%%
monthly = reten.resample('m').sum()
monthly.head()

# %%
x_days = [1,3,7,14,30,60]
y_data = dm.totalRetentionAverage(reten).tolist()

retention_profile = th.create_profile(x_days, y_data[:-1])
th.plot_retention(retention_profile)
#%%
retention = retention_profile['retention_projection'][1]
days = pd.DataFrame(np.arange(0,60))

