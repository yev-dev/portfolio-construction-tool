import abc

from pct.core.parameters import OptimizerParameters

class OptimizeResult(object):
    
    def __init__(self, ):
        super().__init__()


class PortfolioOptimizer(abc.ABC):

    def __init__(self, parameters: OptimizerParameters):
       
        self._parameters = parameters
    
    @property
    def parameters(self):
        return self._parameters

    def optimize(self, df_portfolio):
        
        self._optimize_portfolio(df_portfolio=df_portfolio)

        
    
    @abc.abstractclassmethod
    def _optimize_portfolio(self, df_portfolio):
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
    

class SimplePortfolioReturnOptimizer(PortfolioOptimizer):
    
    def _optimize_portfolio(self, df_portfolio):
        
        return super()._optimize_portfolio(df_portfolio)


class SharpeRationOptimizer(PortfolioOptimizer):
    pass