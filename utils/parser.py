import apimoex
import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor,  as_completed
import streamlit as st

#акции
request_url_shares_sequrities = ('https://iss.moex.com/iss/engines/stock/'
               'markets/shares/boards/TQBR/securities.json')
arguments_shares_sequrities = {'securities.columns': ('SECID,'
                                    'LOTSIZE,'
                                    'SECNAME,'
                                    'ISIN')}

request_url_shares_market_data = ('https://iss.moex.com/iss/engines/stock/'
               'markets/shares/boards/TQBR/securities.json?iss.meta=off&iss.only=marketdata')
arguments_shares_market_data = {'marketdata.columns': ('SECID,'
                                    'OPEN,'
                                    'LOW,'
                                    'HIGH,'
                                    'LAST')}

#облигации
request_url_bonds_sequrities = ('https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?iss.meta=off&iss.only=securities')
arguments_bonds_sequrities = {'securities.columns': ('SECID,'
                                    'SECNAME,'
                                    'FACEVALUE,'
                                    'COUPONVALUE,'
                                    'COUPONPERCENT,'
                                    'ISIN,'
                                    'BOARDID')}

request_url_bonds_market_data = ('https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?iss.meta=off&iss.only=marketdata')
arguments_bonds_market_data = {'marketdata.columns': ('SECID,'
                                    'YIELD,'
                                    'YIELDLASTCOUPON,'
                                    'OPEN,'
                                    'LOW,'
                                    'HIGH,'
                                    'LAST')}

df_shares_sec = pd.DataFrame()
df_shares_mar = pd.DataFrame()

df_bonds_sec = pd.DataFrame()
df_bonds_mar = pd.DataFrame()


#@st.cache_data()
def GetDataFrame(UrlArgType):
    
    with requests.Session() as session:
        try:
            iss = apimoex.ISSClient(session, UrlArgType[0], UrlArgType[1])
            data = iss.get()
            df = pd.DataFrame(data[UrlArgType[2]])
            df.set_index('SECID', inplace=True)
            time.sleep(0.1)
            #print(df.to_string())
        except Exception:
            df = pd.DataFrame(columns=['column1', 'column2', 'column3'])
            return df
    return df

# Shares Bonds
def startParse() -> list[pd.DataFrame, pd.DataFrame]:  #, pd.DataFrame):
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(GetDataFrame, arg) for arg in ((request_url_shares_sequrities, arguments_shares_sequrities, 'securities'), (request_url_bonds_sequrities, arguments_bonds_sequrities, 'securities'))]
        for future in as_completed(futures):
            result = future.result()
            if 'FACEVALUE' not in result.columns.tolist():
                df_shares_sec = result
            else:
                df_bonds_sec = result
                

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures1 = [executor.submit(GetDataFrame, arg) for arg in ((request_url_shares_market_data, arguments_shares_market_data, 'marketdata'), (request_url_bonds_market_data, arguments_bonds_market_data, 'marketdata'))]
        for future in as_completed(futures1):
            result = future.result()
            if 'YIELD' not in result.columns.tolist():
                df_shares_mar = result
            else:
                df_bonds_mar = result

    #2518
    #244
    df_shares_all = pd.concat([df_shares_sec, df_shares_mar], axis=1)
    df_shares_all = df_shares_all.drop_duplicates(subset=['ISIN'])
    df_shares_all = df_shares_all.fillna(0)
    df_shares_all = df_shares_all.loc[df_shares_all.get('LAST') != 0.0000]

    df_bonds_all = pd.concat([df_bonds_sec, df_bonds_mar], axis=1)
    df_bonds_all = df_bonds_all.fillna(0)
    df_bonds_all = df_bonds_all.loc[df_bonds_all["BOARDID"] != "SPOB"]
    df_bonds_all = df_bonds_all.drop_duplicates(subset=['ISIN'])
    df_bonds_all = df_bonds_all.loc[df_bonds_all['LAST'] != 0.0000]

    return [df_shares_all, df_bonds_all]

#l = startParse()[1]

#print(l.to_string())
