import csv
import pandas as pd
import yfinance as yf

from typing import Union, List, Set
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

HISTORICAL_PRICES_COLUMNS = ['date', 'ticker', 'open','high','low','close','volume']

class PriceHistory():

    def __init__(self, tickers: Union[List, Set]) -> None:
        self._tickers = tickers
        self.counter = 0
        self._df_prices = pd.DataFrame()
    
    @property
    def prices(self) -> pd.DataFrame:
        return self._df_prices
    
    @property
    def tickers(self) -> List[str]:  
        return self._tickers
    
    @property
    def size(self) -> int:
        return len(self._df_prices)
    
    @property
    def is_empty(self) -> bool:
        return False if self.size else True
    
    def download_prices(self, from_date: date = None, to_date: date = None) -> None:

        today = datetime.today().date()

        if not from_date:
            from_date = today - relativedelta(months=6)
        
        if not to_date:
            to_date = today
        
        for ticker in self._tickers:
            df_ticker_prices = self._get_prices(
                ticker = ticker,
                from_date = from_date,
                to_date = to_date
            )

            if not df_ticker_prices.empty:
                self._df_prices = self._df_prices.append(df_ticker_prices)

        if self.is_empty:
            return
        
        # Cleaning 
        self._df_prices.columns = [c.lower().replace(' ', '_') for c in self._df_prices.columns]
        
        if not any(['date' in self._df_prices.index, isinstance(self._df_prices.index, pd.DatetimeIndex)]):
            self._df_prices['date'] = pd.to_datetime(self._df_prices['date'])

        
    def save_prices(self, save_fpath: str,  archived = False, columns: List = None) -> None:
        """[summary]

        Args:
            save_fpath (str): path to save a file
            archived (bool, optional): archives to zip if true. Defaults to False.
            from_date (date, optional): [description]. Defaults to None.
            to_date (date, optional): [description]. Defaults to None.
            columns (List, optional): [description]. Defaults to None.
        """

        df = self.prices[columns] if columns else self.prices[HISTORICAL_PRICES_COLUMNS]

        if not df.empty:
            if archived:
                compression_opts = dict(method='zip', archive_name='out.csv')
                df.to_csv('out.zip', compression_opts, index=False)
            else:
                df.to_csv(save_fpath, index=False)
    


    def _get_prices(self, ticker: str, from_date: date, to_date: date) -> pd.DataFrame:
        """[summary]

        Args:
            ticker (str): [description]
            from_date (date): [description]
            to_date (date): [description]

        Returns:
            pd.DataFrame: [description]
        """
        
        ticker_yf = yf.Ticker(ticker)

        df_ticker_return = ticker_yf.history(start = from_date, end = to_date)
        df_ticker_return['ticker']= ticker
        df_ticker_return.reset_index(inplace=True)

        return df_ticker_return
        