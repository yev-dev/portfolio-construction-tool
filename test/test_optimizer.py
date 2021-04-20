import os

from typing import List
from unittest import TestCase
from pct.data.data_reader import SimpleIndexedCSVDataset
from pct.core.optimizer import SimplePortfolioReturnOptimizer

from pct.core.parameters import OptimizerParameters

basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, r'data')

TEST_HISTORICAL_PRICES_FILE_NAME = 'prices.csv'

class TestPortfolioOptimizer(TestCase):

    def setUp(self) -> None:
        prices_fpath = os.path.join(data_dir, TEST_HISTORICAL_PRICES_FILE_NAME)
        ds = SimpleIndexedCSVDataset(fpath=prices_fpath)
        self.df_prices = ds.read()

    
    def test_optimize_portfolio_return_terminates_successfully(self):
        assert len(self.df_prices.index) > 0

        tickers = ['AAPL','MSFT','AMZN','GOOG','FB','WMT','JPM','TSLA','NFLX','ADBE']

        df_portfolio = self.df_prices[self.df_prices['ticker'].isin(['AAPL','MSFT','AMZN'])]
        parameters = build_sample_optimization_parameters(tickers=['AAPL','MSFT','AMZN'])
        optimizer = SimplePortfolioReturnOptimizer(parameters)

        result = optimizer.optimize(df_portfolio=df_portfolio)
        # print(result)
        self.assertEqual(result.success, True)
        self.assertEqual(result.status, 0)
        self.assertEqual(result.message, 'Optimization terminated successfully')


def build_sample_optimization_parameters(tickers: List = None):

    tickers = ['APPL', 'FB'] if not tickers else tickers
    constraints = {'sum_of_weights' : 'eq'}
        
    request = {}
    request[OptimizerParameters.TAG_KEY] = 'scipy_optimizer_v1'
    request[OptimizerParameters.TICKERS_KEY] = tickers
    request[OptimizerParameters.CONSTRAINTS_KEY] = constraints

    return OptimizerParameters(**request)