#%%
from MarketingManager import MarketingManager
from apps import studio_mapping
from apps import app_ids

import pandas as pd 
import numpy as np 

#%%
mm = MarketingManager()

#%%
lib_df = mm.libringDataFrame('2020-02-10','2020-02-14')
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
lib_df.join(dau, on = ['application_cd','date'], how ='left')

# %%
print(len(lib_df))
print(len(dau))

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
df = df.groupby(['app_x','studio'], axis = 1).resample('d').sum()

#%%
df.reset_index(inplace = True)
df = df[['date','app_x','impressions','ad_revenue','TotalDAU','clicks','conversions','studio']]


# %%
df.head()

# %%
df.to_csv('data.csv')

# %%
frozen = df.loc[df['app_x'] == 'Disney Frozen Adventures']

# %%
frozen.head()

# %%
