#%%
from MarketingManager import MarketingManager
from SqlManager import SqlManager

from apps import studio_mapping
from apps import app_ids
from credentials import credentials

import pandas as pd 
import numpy as np 

#%%
host = credentials['mysql_host']
username = credentials['user_name']
password = credentials['mysql_pw']

sql = SqlManager(host, 'ad_revenue', username, password)
sql.connect()
#%%
mm = MarketingManager()

#%%
lib_df = mm.libringDataFrame('2020-01-01','2020-03-21')
#%%
lib_df['application_cd'] = pd.to_numeric(lib_df['application_cd'])
#%%
dau = mm.dataFrameFromFolderPath('dau_data')
#%%
dau['application_cd'] = pd.to_numeric(dau['application_cd'])
dau.head()

# %%
lib_df.head()

# %%
df = lib_df.merge(dau, on=['date', 'application_cd'], how = 'inner')
df.head()

# %%
print(df.columns)
#%%
df.set_index(pd.to_datetime(df['date']), inplace = True)
#%%
df.head()
#%%
# df = df.groupby(['app_x','studio'], axis = 1).resample('d').sum()

#%%
df.reset_index(inplace = True)
#%%
workSheet = df[['date','app_x','impressions','ad_revenue','TotalDAU','clicks','conversions','studio']]

#%%
sql_upload = df[['date','application_cd','app_x','iron_appkey','platform','studio','impressions','ad_revenue','TotalDAU','clicks','conversions']]
sql_upload.rename(columns = {
    'app_x': 'application_cd',
    'iron_appkey': 'appkey',
    'TotalDAU': 'dau'}, inplace = True)
sql.connect()
sql.upload_to_db(sql_upload, 'libring_revenue', 'replace')

# %%
df.head()

# %%
df.to_csv('data.csv')



# %%
