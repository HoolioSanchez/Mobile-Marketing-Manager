"""
Main class to manage all API request from 3rd parties
"""
import requests 
from credentials import credentials

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
            return res.text


