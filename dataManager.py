
import pandas as pd
from pandas.io.json import json_normalize
from Data import Data
import matplotlib.pyplot as plt

data = Data()
ironsource = data.getIronsourceData('2020-02-10', '2020-02-15')
libring = data.getLibringData('2020-02-10','2020-02-15')
dau = data.getDailyActiveUsers()

df = pd.DataFrame(ironsource)
df.head()

print(df.columns)

def flattenData(dataframe):
    temp = []
    for item in dataframe.data:
        j_obj = json_normalize(item)
        temp.append(j_obj)
 
    return pd.concat(temp)
