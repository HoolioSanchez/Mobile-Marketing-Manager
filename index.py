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
data = DataManager()
th = th.theseus()

#%%
df = data.ironsourceDataFrame('2019-12-01', '2019-12-31')

#%%
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

panda = df[df['appName'].str.contains('Panda')]
pp_rev = panda['revenue'].resample('d').sum()
pp_rev = pp_rev.reset_index()
pp_rev = pp_rev.drop('date', axis = 1)
pp_rev.head()

#%%
reten = data.retentionDataFrame('rentention_data')
reten.set_index('INSTALL_DT', inplace = True)
reten = data.calculateRetentionPct(reten)
reten.head()

#%%
dau = data.dailyActiveUserDataframe('dau_data')
dau.head()
#%%


#%%
def getInstallCohort(dataframe, param):
    temp = []
    for i in dataframe[param]:
        temp.append(i)
    
    return temp

#%%
x_data = [1,7,14,30,60]
y_values = getTotalRetentionAverage(reten)

#%%
print(y_values)
#%%
ww = th.create_profile(x_data, y_values.tolist())

#%%
print(ww)

#%%
x = ww['retention_projection']
#%%
rentention = [100.0, 31.997537739240748, 22.568526071212478, 19.815265216855344, 18.14416051944073, 16.940702269056708, 15.999587684977019, 15.226662566900636, 14.57082916745627, 14.001233821426126, 13.497810161543816, 13.04677127245032, 12.638235365184578, 12.264877355800502, 11.921116477393701, 11.602602948152818, 11.305880601106217, 11.028157716320125, 10.76714691040071, 10.520950524834081, 10.287976828673912, 10.066877599198454, 9.85650085242342, 9.655854514555054, 9.464078129509506, 9.280420559424387, 9.10422221653237, 8.934900764461814, 8.771939506492663, 8.614877876744647]

#%%
th.plot_retention(ww)

#%%
cohort = getInstallCohort(reten, 'INSTALL_QTY')
print(cohort)
#%%
ww_dau = th.project_cohorted_DAU(profile = ww, periods = 50, cohorts = cohort, start_date=1)
print(ww_dau)

#%%
new_users = th.get_DNU(ww_dau)
print(new_users)

#%%
ww_totals = th.DAU_total(ww_dau)
# %

# %%
ww_totals.head()

# %%
ww_totals.to_csv('dau_projection.csv')

# %%
arpu = pp_rev['revenue']/dau['DAU']
#%%
arpu.head()
# %%
rentention_numpy = np.array(rentention)
#%%
print(rentention_numpy)
#%%
churn_users = (100 - rentention_numpy)
print(churn_users)
#%%
ltv = arpu[:30] * rentention_numpy

# %%
ltv.head(30)

# %%
ltv.plot()
plt.yscale("log")
plt.show()

# %%
