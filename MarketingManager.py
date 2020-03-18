
#%%
import pandas as pd
from pandas.io.json import json_normalize
from Data import Data
import matplotlib.pyplot as plt
import numpy as np
from apps import app_ids
#%%
class MarketingManager:
    data = Data()
    def ironsourceDataFrame(self, startDate, endDate):
        """
        Returns a Pandas DataFrame from Ironsource API

        Arguments: 
        startDate = required start date
        endDate = required end date

        Returns: 
            Pandas Dataframe: json normalized dataframe

        """
        meta_params = ['adUnits','appKey', 'appName', 'bundleId','date']
        return json_normalize(self.data.getIronsourceData(startDate, endDate), 'data', meta = meta_params)


    def libringDataFrame(self, startDate, endDate): 
        """
        Returns a Pandas DataFrame from Libring API

        ParaArgumentsms: 
        startDate = required start date
        endDate = required end date

        Returns: 
            Pandas Dataframe
        """
        temp = []
        libring = self.data.getLibringData(startDate, endDate)

        for index in libring['connections']: 
            for app in app_ids:
                if index['app'] == app:
                    if index['platform'] == 'Android':
                        index.update({
                            'app_cd_name': app_ids[app]['app_cd_name'],
                            'studio': app_ids[app]['studio'],
                            'application_cd': app_ids[app]['app_cd_android'],
                            'iron_appkey': app_ids[app]['iron_appkey_android']
                        })
                        temp.append(index)
                    if index['platform'] == 'iOS':
                        index.update({
                            'app_cd_name': app_ids[app]['app_cd_name'],
                            'studio': app_ids[app]['studio'],
                            'application_cd': app_ids[app]['app_cd_ios'],
                            'iron_appkey': app_ids[app]['iron_appkey_ios']
                        })
                        temp.append(index)

        return pd.DataFrame(temp)


    def dataFrameFromFolderPath(self, path):
        """
        returns a dataframe from a csv folder path

        Arguments:
            path to folder containing csv files 
        
        Returns: 
            Pandas Dataframe - containing csv data
        """
        return self.data.getCSVFolder(path)
    
    def calculateRetentionPct(self, dataframe):
        """
        Adds Retention percentage for Day 1,7,14,and 90 to Dataframe

        Arguments:
            dataframe - pandas dataframe containing 'RETENTION_1_QTY' to 'RETENTION_90_QTY' 
        
        Returns: 
            Pandas Dataframe - containing the mean
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
        Returns a LTV dataframe using a simple model. 

        Formula: 
        LTV = <ARPDAU> * TotalDaysPlayed
        TotalsDaysPlayed = (1/a-1)*(1-D^(1-a))

        Arguments: 
        days -  array of days cohort
        retention - retention values of cohort
        arpdau - average revenue per daily active user

        Returns: 
            Pandas Dataframe - containing days, retention, totalDaysPlayed, and LTV

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

    def coef_retention_curve(self, n_days, n_retention):
        """
        Returns the values for a and b in a power function:
        y = a*x^b

        Arguments:
        n_days - array of days cohort (ignores day 0)
        n_retention - retention values of cohort (ignores day 0)

        Returns: 
            float: a,b 
        """

        log_days = np.log(n_days)
        log_retention = np.log(n_retention)

        a = np.exp(np.polyfit(log_days[1:], log_retention[1:], 1))
        a = a[1]

        b = np.polyfit(log_days[1:], log_retention[1:], 1)
        b = b[0]

        return a,b
    
    def project_retention_rates(self, n_days_to_project, days, retention):
        """
        Uses a power function to calculate the projected retention rates for given n_days. 

        Formula:
        y = a*x^b

        Arguments: 
        n_days_to_project - the number of days to project too.
        days - original days cohort relative to retention values
        retention - retention values of cohort (ignores day 0)

        Returns: 
            list - projected values for retention
        """

        start = days[-1]
        end = n_days_to_project
        day = np.arange(start, end)

        a,b = self.coef_retention_curve(days, retention)

        projected_retention = retention

        for index in day: 
            y = a * index ** b
            projected_retention.append(y)
        
        return projected_retention
