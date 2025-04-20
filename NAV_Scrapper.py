###################

TEST = False

###################

import os
import httpx
import asyncio
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import date
from aiolimiter import AsyncLimiter

PARENT_DIR = Path(__file__).parent
DB_PATH = PARENT_DIR / 'DB_Instance'
JSON_PATH = PARENT_DIR / 'data.json'
DATE = f'{date.today().year:04}-{date.today().month:02}-{date.today().day:02}'

os.makedirs(DB_PATH, exist_ok = True)
ticker_File =  PARENT_DIR / 'Ticker_Info.csv'
holdings_File =  PARENT_DIR / 'holdings-XXXXXX.xlsx'

ticer_df = pd.read_csv(ticker_File)
holdings_df = pd.read_excel(holdings_File, sheet_name = 'Combined', skiprows = 22,
                            usecols = ['Symbol', 'ISIN', 'Quantity Available', 'Average Price'])
holdings_df.loc[holdings_df.Symbol == 'INE01TI01010', 'ISIN'] = 'INE01TI01010'
holdings_df.loc[holdings_df.Symbol == 'INE01TI01010', 'Symbol'] = 'VPS Lakeshore'
merged_df = holdings_df.merge(ticer_df, on = 'ISIN')
merged_df.drop(['Symbol_x', 'Name'], axis = 1, inplace = True)
merged_df.rename(columns = {'Symbol_y' : 'Symbol',
                            'Quantity Available' : 'Quantity',
                            'Average Price' : 'Average_Price'}, inplace = True)

async def getClose(client, url, limiter):
    try:
        ticker = url.split('-')[-1].strip()
    except: return None
    async with limiter:
        if not TEST:
            try:
                API = f'https://quotes-api.tickertape.in/quotes?sids={ticker}'
                response = await client.get(API)
                if response.status_code == 200:
                    data = response.json().get('data')[0]
                    return data.get('c')
            except:
                try:
                    API = f'https://api.tickertape.in/mutualfunds/{ticker}/info'
                    response = await client.get(API)
                    if response.status_code == 200:
                        data = response.json().get('data')
                        return data.get('navClose')
                except: return None
        else:
            return 0

async def scrapper():
    rate_limiter = AsyncLimiter(max_rate = 20, time_period = 5)
    async with httpx.AsyncClient() as client:
        tasks = [getClose(client, url, rate_limiter) for url in merged_df.URL.values]
        results = await asyncio.gather(*tasks)
    return results

merged_df['Date'] = DATE
merged_df['NAV'] = asyncio.run(scrapper())

merged_df = merged_df[['ISIN', 'Symbol', 'Quantity', 'Average_Price', 'NAV', 'Date']]

if not TEST:
    with sqlite3.connect(DB_PATH/'folio_NAV.db') as conn:
        merged_df.to_sql(name = 'nav_data', con = conn, if_exists = 'append',
                         index = False, dtype = {'ISIN' : 'TEXT', 'Quantity' : 'REAL',
                                                 'Symbol' : 'TEXT', 'Date' : 'TEXT',
                                                 'NAV' : 'REAL', 'Average_Price' : 'REAL'})
else:
    missing_ = set(holdings_df.ISIN.values) - set(ticer_df.ISIN.values)
    assert len(missing_) == 0, f"Missing tickers are :: {missing_}"

merged_df.to_json(JSON_PATH)
