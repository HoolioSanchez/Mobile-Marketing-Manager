
#%%
import pandas as pd
from pandas.io.json import json_normalize
from Data import Data
import matplotlib.pyplot as plt

data = Data()


# dau = data.getDailyActiveUsers()

def ironsourceDataFrame(startDate, endDate):
    """
    Returns a Pandas DataFrame from Ironsource API

    Params: 
    startDate = required start date
    endDate = required end date
    """
    meta_params = ['adUnits','appKey', 'appName', 'bundleId','date']
    return json_normalize(data.getIronsourceData(startDate, endDate), 'data', meta = meta_params)


# %%
def libringDataFrame(startDate, endDate): 
    """
    Returns a Pandas DataFrame from Libring API

    Params: 
    startDate = required start date
    endDate = required end date
    """
    libring = data.getLibringData(startDate, endDate)
    return pd.DataFrame(libring)


