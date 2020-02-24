#%%
from Data import Data
import pandas as pd
import matplotlib.pyplot as plt


#%%
data = Data()

df = data.getRetention('retention_data')

df.head()

# %%
df.set_index('INSTALL_DT', inplace = True)

#%%

def calculateRetentionPct(dataframe):
    dataframe['Day_1_Pct'] = dataframe.RETENTION_1_QTY/dataframe.INSTALL_QTY
    dataframe['Day_7_Pct'] = dataframe.RETENTION_7_QTY/dataframe.INSTALL_QTY
    dataframe['Day_14_Pct'] = dataframe.RETENTION_14_QTY/dataframe.INSTALL_QTY
    dataframe['Day_90_Pct'] = dataframe.RETENTION_90_QTY/dataframe.INSTALL_QTY



# %%
cookiejam = df.loc[df['APPLICATION_FAMILY_NAME'] == 'Cookie Jam']

# %%
cookiejam.head()

# %%
cookiejam.index = pd.to_datetime(cookiejam.index)

# %%
cookiejamOverview = cookiejam.resample('d').sum()

# %%
cookiejamOverview.drop('APPLICATION_CD', axis = 1, inplace = True)

# %%
calculateRetentionPct(cookiejamOverview)
cookiejamOverview.head()


# %%
cookieGraph = cookiejamOverview[['Day_1_Pct','Day_7_Pct','Day_14_Pct' 'Day_90_Pct']]