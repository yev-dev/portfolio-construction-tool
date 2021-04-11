import os

from unittest import TestCase

from pct.data.data_reader import SimpleIndexedCSVDataset

basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, r'data')

TEST_HISTORICAL_PRICES_FILE_NAME = 'prices.csv'

class TestDatasetReader(TestCase):

    def test_load_stock_prices(self):
        prices_fpath = os.path.join(data_dir, TEST_HISTORICAL_PRICES_FILE_NAME)
        ds = SimpleIndexedCSVDataset(fpath=prices_fpath)
        df = ds.read()
        self.assertTrue(len(df.index) > 0)
    
    def test_pivoting_after_load_stock_prices(self):
        prices_fpath = os.path.join(data_dir, TEST_HISTORICAL_PRICES_FILE_NAME)
        ds = SimpleIndexedCSVDataset(fpath=prices_fpath)
        df_prices = ds.read()
        df_prices.reset_index(inplace=True)
        df_prices = df_prices.pivot(index='date', columns='ticker', values='close')

        self.assertEqual(df_prices.index.name, 'date' )
        self.assertAlmostEqual(df_prices.loc['2020-10-07', 'AAPL'], 114.71038818359376)
