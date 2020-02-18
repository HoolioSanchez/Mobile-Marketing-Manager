#%%
import os
import pandas as pd
from Data import Data

#%%

data = Data()
# ironsource = data.getIronsourceData('2020-02-10', '2020-02-15')
# libring = data.getLibringData('2020-02-10','2020-02-15')
# dau = data.getDailyActiveUsers()

data.getAdmobData()

# %%
