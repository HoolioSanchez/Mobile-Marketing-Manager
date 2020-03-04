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
ad_rev = dm.ironsourceDataFrame('2019-12-01','2019-12-31')
#%%
ad_rev['date'] = pd.to_datetime(ad_rev['date'])
ad_rev.set_index('date', inplace=True)
panda = ad_rev[ad_rev['appName'].str.contains('Panda')]
pp_rev = panda['revenue'].resample('d').sum()
pp_rev = pp_rev.reset_index()
pp_rev = pp_rev.drop('date', axis = 1)
pp_rev.head()
#%%
dau = dm.dailyActiveUserDataframe('dau_data')
dau.head()

#%%
pp_rev['arpdau'] = pp_rev['revenue'] / dau['DAU']
#%%
pp_rev.head()
#%%
reten = dm.retentionDataFrame('rentention_data')
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
retention_projection = retention_profile['retention_projection'][1]
profile = pd.DataFrame(retention_projection)
profile.to_csv('retention_pro.csv')
# %%
print(len(retention_projection))

# %%
days = np.arange(0,366)
#%%
reg = LinearRegression().fit(retention_projection)
# reg.score(days[0:60], retention_projection)

# %%
retention_days = days[:60]

#%%
log_days = np.log(retention_days)
log_retention = np.log(retention_projection)
# %%
area = log_retention/log_days
#%%
a = area[-1]
#%%
print(a)
#%%
user_lifetime = []
for index in days:
    agg = (1/(a - 1) * (1 - index ** (1-a)))
    user_lifetime.append(agg)

print(user_lifetime)

#%%
# arpdu = float(monthly['AD_REVENUE'] / monthly['INSTALL_QTY'])
arpdu = pp_rev['arpdau'].mean()
print(arpdu)
# %%
ltv = []
for item in user_lifetime:
    lagg = item * arpdu
    ltv.append(lagg)

#%%
print(ltv)

# %%
plt.plot(days, ltv)
plt.show()

# %%
LTV_df = pd.DataFrame({
    'days': days,
    'user_lifetime': user_lifetime,
    'LTV': ltv,
})
LTV_df.to_csv('panda_ads_ltv_dec.csv')


# %%
average_rev = reten['AD_REVENUE'] / reten['INSTALL_QTY']

# %%
average_rev.head()



# %%
average_rev.to_csv('ad_rev_per_install.csv')

# %%
