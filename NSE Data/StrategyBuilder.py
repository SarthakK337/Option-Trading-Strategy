import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for
import math #The Python math module
import pandas as pd
import json
from pandas import json_normalize

class Strategys:
    def __init__(self):
        self.headers={ 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        self.session=requests.session()
        self.session.get("http://nseindia.com", headers = self.headers)

    def option_data(self, symbol, Expiry, indices=True):
        symbol=symbol.replace(',' ,'%20').replace('&', '%26')
        if not indices:
            url = 'https://www.nseindia.com/api/option-chain-equities?symbol=' + symbol
        else:
            url = 'https://www.nseindia.com/api/option-chain-indices?symbol=' + symbol
        json_obj = self.session.get(url, headers=self.headers).json()
        # data = self.session.get(url, headers =self.headers).json()["records"]["data"]
        # my_df = []
        # for i in data:
        #     for k, v in i.items():
        #         if k =="CE" or k == "PE":
        #             info = v
        #             info["instrumentType"] = k
        #             my_df.append(info)
        # df = pd.DataFrame(my_df)
        # df = df.set_index("identifier", drop=True)
        data = json_normalize(json_obj["records"]["data"])
        data["expiryDate"]= pd.to_datetime(data["expiryDate"])
        df=data[data["expiryDate"]==Expiry]
        return df

    def StrikePrice(self, symbol , Expiry):
        try:
            Data = self.option_data(symbol, Expiry)
            df = Data["PE.underlyingValue"].iloc[0]
        except Exception as e:
            return e
        else:
            return df


    def CallPrice(self, symbol , Expiry, StrikePrice):
        try:
            Data=self.option_data(symbol, Expiry)
            df = Data[Data["CE.strikePrice"] == StrikePrice]["CE.lastPrice"].iloc[0]
        except Exception as e:
            return e
        else:
            return df

    def PutPrice(self, symbol , Expiry, StrikePrice):
        try:
            Data = self.option_data(symbol, Expiry)
            df = Data[Data["PE.strikePrice"] == StrikePrice]["PE.lastPrice"].iloc[0]
        except Exception as e:
            return e
        else:
            return df

    def CE_OpenInterest(self, symbol , Expiry, StrikePrice):
        try:
            Data = self.option_data(symbol, Expiry)
            df = Data[Data["CE.strikePrice"] == StrikePrice]["CE.openInterest"].iloc[0]
        except Exception as e:
            return e
        else:
            return df

    def PE_OpenInterest(self, symbol , Expiry, StrikePrice):
        try:
            Data = self.option_data(symbol, Expiry)
            df = Data[Data["PE.strikePrice"] == StrikePrice]["PE.openInterest"].iloc[0]
        except Exception as e:
            return e
        else:
            return df

class ShortIronCondor(Strategys):

    def MaxProfit(self, symbol , Expiry, CE_strikePrice_Sell,PE_strikePrice_Sell,CE_strikePrice_Buy,PE_strikePrice_Buy):
        try:
            self.CE_Sell = self.CallPrice(symbol, Expiry, CE_strikePrice_Sell)
            self.PE_Sell = self.PutPrice(symbol, Expiry, PE_strikePrice_Sell)
            self.CE_Buy = self.CallPrice(symbol, Expiry, CE_strikePrice_Buy)
            self.PE_Buy = self.PutPrice(symbol, Expiry, PE_strikePrice_Buy)
            self.max=round((self.CE_Sell+self.PE_Sell-self.CE_Buy-self.PE_Buy)*50,2)
        except Exception as e:
            return str(e)
        else:
            return self.max

    def MaxLoss(self, symbol , Expiry, CE_strikePrice_Sell,PE_strikePrice_Sell,CE_strikePrice_Buy,PE_strikePrice_Buy):
        try:
            self.CE_Sell = self.CallPrice(symbol, Expiry, CE_strikePrice_Sell)
            self.PE_Sell = self.PutPrice(symbol, Expiry, PE_strikePrice_Sell)
            self.CE_Buy = self.CallPrice(symbol, Expiry, CE_strikePrice_Buy)
            self.PE_Buy = self.PutPrice(symbol, Expiry, PE_strikePrice_Buy)
            self.PointDIff= max(CE_strikePrice_Buy-CE_strikePrice_Sell,PE_strikePrice_Buy-PE_strikePrice_Sell)
            self.max= round((self.CE_Sell + self.PE_Sell - self.CE_Buy - self.PE_Buy - self.PointDIff) * 50, 2)

        except Exception as e:
            return str(e)

        else:
            return self.max

    def RiskReward(self, symbol , Expiry, CE_strikePrice_Sell, PE_strikePrice_Sell, CE_strikePrice_Buy, PE_strikePrice_Buy):
        try:
            self.ans=round(-(self.MaxLoss(symbol , Expiry, CE_strikePrice_Sell, PE_strikePrice_Sell, CE_strikePrice_Buy, PE_strikePrice_Buy))
                           /self.MaxProfit(symbol , Expiry, CE_strikePrice_Sell, PE_strikePrice_Sell, CE_strikePrice_Buy, PE_strikePrice_Buy)
                           ,2)
        except Exception as e:
            return str(e)

        else:
            return self.ans









