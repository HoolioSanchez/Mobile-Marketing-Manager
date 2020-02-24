
#%%
import pandas as pd
from pandas.io.json import json_normalize
from Data import Data
import matplotlib.pyplot as plt

#%%
class DataManager:
    data = Data()
    def ironsourceDataFrame(self, startDate, endDate):
        """
        Returns a Pandas DataFrame from Ironsource API

        Params: 
        startDate = required start date
        endDate = required end date
        """
        meta_params = ['adUnits','appKey', 'appName', 'bundleId','date']
        return json_normalize(self.data.getIronsourceData(startDate, endDate), 'data', meta = meta_params)

   
    def libringDataFrame(self, startDate, endDate): 
        """
        Returns a Pandas DataFrame from Libring API

        Params: 
        startDate = required start date
        endDate = required end date
        """
        temp = []
        libring = self.data.getLibringData(startDate, endDate)

        for item in libring['connections']: 
            print(item)
            temp.append(item)

        return pd.DataFrame(temp)
    
    def calculateRetentionPct(self, dataframe):
        dataframe['Day_1_Pct'] = dataframe.RETENTION_1_QTY/dataframe.INSTALL_QTY
        dataframe['Day_7_Pct'] = dataframe.RETENTION_7_QTY/dataframe.INSTALL_QTY
        dataframe['Day_14_Pct'] = dataframe.RETENTION_14_QTY/dataframe.INSTALL_QTY
        dataframe['Day_90_Pct'] = dataframe.RETENTION_90_QTY/dataframe.INSTALL_QTY


    

