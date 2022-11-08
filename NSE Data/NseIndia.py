import requests
import pandas as pd

class NSE():
    def __init__(self):
        self.headers={ 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        self.session=requests.session()
        self.session.get("http://nseindia.com", headers = self.headers)


    def option_data(self, symbol, indices=False):
        symbol=symbol.replace(',' ,'%20').replace('&', '%26')
        if not indices:
            url = 'https://www.nseindia.com/api/option-chain-equities?symbol=' + symbol
        else:
            url = 'https://www.nseindia.com/api/option-chain-indices?symbole=' + symbol
        data = self.session.get(url, headers =self.headers).json()["records"]["data"]
        my_df = []
        for i in data:
            for k, v in i.items():
                if k =="CE" or k == "PE":
                    info = v
                    info["instrumentType"] = k
                    my_df.append(info)
        df = pd.DataFrame(my_df)
        df = df.set_index("identifier", drop=True)
        return df