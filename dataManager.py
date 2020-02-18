#%%
import os
import pandas as pd
from Data import Data


# data = Data()
# data.getIronsourceData('2020-02-10', '2020-02-15')

"/Users/juliosanchez/Documents/dashboard/dau_data/export.csv"

#%%
def getDailyActiveUsers():
    temp = []
    folderName = 'dau_data'
    folder = os.getcwd() + '/' + folderName
    for sub, dirs, files in os.walk(folder):
        for file in files:
            df = pd.read_csv(os.path.join(sub, file))
            temp.append(df)
    return pd.concat(temp)

dau = getDailyActiveUsers()
dau.head()

# %%
