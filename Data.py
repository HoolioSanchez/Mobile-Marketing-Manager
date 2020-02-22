"""
Main class to manage all API request from 3rd parties
"""
import requests 
import os
import pandas as pd
from pandas.io.json import json_normalize
from credentials import credentials
# from apiclient import sample_tools
# from oauth2client.service_account import ServiceAccountCredentials
# from googleapiclient.discovery import build
# import httplib2

class Data:
    
    def __ironsourceBearerAuth(self):
        """
        Bearer API authentication is needed for the use of ironSource’s Application API and Instance API.
        GET platform.ironsrc.com/partners/publisher/auth
        """
        url = "https://platform.ironsrc.com/partners/publisher/auth"
        header ={
            "secretkey": credentials['ironsource_key'],
            "refreshToken": credentials['ironsource_token']
        }
        res = requests.request("GET", url = url, headers=header)
        
        return res.text

    def getIronsourceData(self, startDate, endDate): 
            """
            Ironsource request:
            GET  platform.ironsrc.com/partners/publisher/mediation/applications/v6/stats?
            """

            url = "https://platform.ironsrc.com/partners/publisher/mediation/applications/v6/stats?"

            queryString = {
                "startDate": startDate,
                "endDate": endDate,
                "breakdown": 'app'
            }

            auth = self.__ironsourceBearerAuth()
        
            headers = {
                "cache-control": "no-cache",
                "Authorization": "Bearer " + auth[1:-1]
            }
            payload = ""

            res = requests.request("GET", url, data = payload, headers = headers, params = queryString)
            print(res.text)
            return res.json()
    
    def getLibringData(self, startDate, endDate):
        """
        Libring request API:
        https://api.libring.com/v2/reporting/get

        Auth: 
        token	‘Authorization’=>”Token TOKEN_CODE”
        """

        url = "https://api.libring.com/v2/reporting/get"

        queryString = {
            "period": "custom_date",
            "start_date": startDate,
            "end_date": endDate,
            "group_by": "date,app"
        }

        headers = {
            "cache-control": "no-cache",
            "Authorization": "Token " + credentials['libring_token']
        }
        payload = ''

        res = requests.request('GET', url, headers = headers, params = queryString, data = payload)
        
        print(res.text)

        return res.json()

    def getDailyActiveUsers(self):
    # "/Users/juliosanchez/Documents/dashboard/dau_data/export.csv"
        temp = []
        folderName = 'dau_data'
        folder = os.getcwd() + '/' + folderName

        for sub, dirs, files in os.walk(folder):
            for file in files:
                df = pd.read_csv(os.path.join(sub, file))
                
                temp.append(df)
        return pd.concat(temp)

    # def __admobBearerAuth(self):

    #     creds = ServiceAccountCredentials.from_json_keyfile_name('admob-api.json', scopes= "https://www.googleapis.com/auth/admob.report")
    #     accessToken = creds.get_access_token()

    #     return accessToken.access_token
       
    # def getAdmobData(self):
    #     url = "https://admob.googleapis.com/v1/accounts/pub-1694638389384549"

    #     headers = {
    #         "Authorization": "Bearer " + self.__admobBearerAuth()
    #     }

    #     payload = ''

    #     res = requests.request("GET", url, headers = headers, data = payload)

    #     print(res.text)