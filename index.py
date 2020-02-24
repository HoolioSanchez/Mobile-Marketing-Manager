#%%
from dataManager import DataManager
import pandas as pd 

data = DataManager()

#%%
df = data.ironsourceDataFrame('2020-02-01', '2020-02-02')

#%%
reten = data.retentionDataFrame('rentention_data')


# %%
reten.head()

# %%
