import abc

import pandas as pd

from pct.util.exceptions import DataLoadingException


class DatasetReader(abc.ABC):

    def __init__(self, fpath):
        self._fpath = fpath
    
    def read(self):
        
        df = self._read(self._fpath)

        if not isinstance(df.index, pd.DatetimeIndex):
            raise DataLoadingException(f"{self._fpath} does not have a valid datetime index")

        return df.sort_index()

    
    @abc.abstractmethod
    def _read(self,fpath):
        """Subclass must specify how to parse the file contents.

        Args:
            fpath (str): Dataset source location
        """
        pass
    
    
class SimpleIndexedCSVDataset(DatasetReader):

    def _read(self,fpath):
        df = pd.read_csv(fpath, parse_dates=['date'], index_col=0)
        return df