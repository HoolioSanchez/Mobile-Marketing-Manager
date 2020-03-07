
#%%
import pandas as pd
from pandas.io.json import json_normalize
from Data import Data
import matplotlib.pyplot as plt
import numpy as np

#%%
class MarketingManager:
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

    def retentionDataFrame(self, path):
        return self.data.getRetention(path)
    
    def dailyActiveUserDataframe(self, path):
        return self.data.getDailyActiveUsers(path)
    
    def calculateRetentionPct(self, dataframe):
        """
        Adds Retention percentage for Day 1,7,14,and 90 to Dataframe

        Required Param: 
        Pandas Dataframe
        """
        dataframe['Day_1_Pct'] = dataframe.RETENTION_1_QTY/dataframe.INSTALL_QTY
        dataframe['Day_3_Pct'] = dataframe.RETENTION_3_QTY/dataframe.INSTALL_QTY
        dataframe['Day_7_Pct'] = dataframe.RETENTION_7_QTY/dataframe.INSTALL_QTY
        dataframe['Day_14_Pct'] = dataframe.RETENTION_14_QTY/dataframe.INSTALL_QTY
        dataframe['Day_30_Pct'] = dataframe.RETENTION_30_QTY/dataframe.INSTALL_QTY
        dataframe['Day_60_Pct'] = dataframe.RETENTION_60_QTY/dataframe.INSTALL_QTY
        dataframe['Day_90_Pct'] = dataframe.RETENTION_90_QTY/dataframe.INSTALL_QTY

        return dataframe
    
    def totalRetentionAverage(self, dataframe):
        temp = []
        day_1 = dataframe['Day_1_Pct'].mean().mean()
        day_3 = dataframe['Day_3_Pct'].mean().mean()
        day_7 = dataframe['Day_7_Pct'].mean().mean()
        day_14 = dataframe['Day_14_Pct'].mean().mean()
        day_30 = dataframe['Day_30_Pct'].mean().mean()
        day_60 = dataframe['Day_60_Pct'].mean().mean()
        day_90 = dataframe['Day_90_Pct'].mean().mean()

        temp.append(day_1)
        temp.append(day_3)
        temp.append(day_7)
        temp.append(day_14)
        temp.append(day_30)
        temp.append(day_60)
        temp.append(day_90)

        np_array = np.array(temp) * 100

        return np_array.astype(int) 
    
    def LTV_Model_1(self, days,retention, arpdau):
        """
        Modeling ARPDAU using the following formula: 
        LTV = <ARPDAU> * TotalDaysPlayed

        TotalsDaysPlayed = (1/a-1)*(1-D^(1-a))

        And, returning a Pandas Dataframe: 
        days, retention, totalDaysPlayed, LTV

        Required_Params: 
        Days = array of days cohort
        retention = retention values of cohort
        arpdau = average revenue per daily active user
        """

        log_days = np.log(days)
        log_retention = np.log(retention)

        area = log_retention/log_days
        a = area[-1]

        totalsDaysPlayed = []

        for index in days:
            daysPlayed  = (1/(a - 1) * (1 - index ** (1-a)))
            totalsDaysPlayed .append(daysPlayed )
        
        ltv = []
        
        for played in totalsDaysPlayed: 
            ltv_formula = arpdau * played
            ltv.append(ltv_formula)

        ltv_df = pd.DataFrame({
        'Days': days,
        'Retention': retention,
        'TotalsDaysPlayed': totalsDaysPlayed,
        'LTV': ltv,})

        ltv_df.set_index('Days', inplace=True)

        return ltv_df




    

