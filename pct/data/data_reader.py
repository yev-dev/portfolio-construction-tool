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

        def __str__(self):
        return self.__repr__()

    def __repr__(self):

        attrs_list = ["{}={!r}".format(attr_name, getattr(self, attr_name))
                      for attr_name in self._attributes
                      if getattr(self, attr_name) is not None]

        attrs = ", ".join(attrs_list)
        cls_name = self, __class__.__name__
        return "{}({})".format(cls_name, attrs)

class SimpleIndexedCSVDataset(DatasetReader):

    def _read(self,fpath):
        df = pd.read_csv(fpath, parse_dates=['date'], index_col=0)
        return df