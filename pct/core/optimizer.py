import abc
import logging
import pandas as pd
import numpy as np

from dataclasses import dataclass
from typing import Dict, List

from scipy import optimize as sci_opt
from pct.core.parameters import OptimizerParameters
from pct.util.exceptions import OptimizationParametersException, PortfolioOptimizationException

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult(object):
    
    success: str
    status: str
    message: str
    weights: Dict
    


class PortfolioOptimizer(abc.ABC):

    def __init__(self, parameters: OptimizerParameters) -> None:
        self._parameters = parameters
    
    @property
    def parameters(self) -> OptimizerParameters:
        return self._parameters
    
    @property
    def fields(self):
        return ['ticker', 'close']
    
    def optimize(self, df_portfolio) -> OptimizationResult:
        logger.info(f"Starting ")

        # Normalize and validate data
        df = self._prepare_portfolio(df_portfolio=df_portfolio)
        result = self._optimize_portfolio(df_portfolio=df)
        return result

    @abc.abstractclassmethod
    def _prepare_portfolio(self, df_portfolio) -> pd.DataFrame:
        """Normalize and validates portfolio dataframe

        Args:
            df_portfolio ([DataFrame]): [description]

        Returns:
            pd.DataFrame: Portfolio ready to be optimized
        """
        pass
    
    @abc.abstractclassmethod
    def _optimize_portfolio(self, df_portfolio) -> OptimizationResult:
        pass


class SimplePortfolioReturnOptimizer(PortfolioOptimizer):

    def _prepare_portfolio(self, df_portfolio) -> pd.DataFrame:

        logger.info(f"Preparing portfolio")
        
        df_portfolio.columns = [c.lower().replace(' ', '_') for c in df_portfolio.columns]
        columns = df_portfolio.columns

        if not all(item in columns for item in self.fields):
            raise PortfolioOptimizationException(f"Missing manadatory {self.fields} in portfolio")

        if not isinstance(df_portfolio.index, pd.DatetimeIndex):
            raise PortfolioOptimizationException(f"Portfolio does not have DatetimeIndex index")

        df_portfolio = df_portfolio[self.fields]
        df_portfolio.reset_index(inplace=True)
        df_portfolio = df_portfolio.pivot(index='date', columns='ticker', values='close')

        # Different scales - normalize to star with 1
        df_portfolio = df_portfolio / df_portfolio.iloc[0]

        logger.info(f"Number of records to process {len(df_portfolio.index)}")
        return df_portfolio


    def _optimize_portfolio(self, df_portfolio) -> OptimizationResult:
        
        opt_parameters = self.parameters.params

        logger.debug(opt_parameters)

        def portfolio_returns(weights, df_portfolio):
            # Distribute allocation by weights
            df_portfolio = df_portfolio * weights
            portfolio_return = df_portfolio.sum(axis=1)
            portfolio_return = portfolio_return[-1]

            # Minimum is a maximum, we need to negate as SciPy optimizer can only minimize
            return -portfolio_return


        try:
            tag = opt_parameters[OptimizerParameters.TAG_KEY]
            method = opt_parameters[OptimizerParameters.METHOD_KEY]

            tickers = opt_parameters[OptimizerParameters.TICKERS_KEY]
            initial_weights = opt_parameters[OptimizerParameters.INITIAL_WEIGHTS_KEY]
            bounds = opt_parameters[OptimizerParameters.BOUNDS_KEY]
            constraints = opt_parameters[OptimizerParameters.CONSTRAINTS_KEY]

            optimized_allocation = sci_opt.minimize(
                fun=portfolio_returns, # Function that we use to minimize
                x0 = initial_weights, # Starting value. Equal allocation
                args=df_portfolio, 
                method=method,
                bounds=bounds, 
                constraints=constraints
            )

        except (OptimizationParametersException, ValueError) as e:
            msg = f"Failed to extract all required parameters for {tag}"
            logger.error(msg)
            raise PortfolioOptimizationException(msg) from e
        else:
            optimized_weights = { t:round(a[1]) for t,a in zip(tickers, np.ndenumerate(optimized_allocation['x']))}

            logger.debug(f"Optimized weights {optimized_weights}")

            result = OptimizationResult(
                success = str(optimized_allocation.success),
                status = optimized_allocation.status,
                message = optimized_allocation.message,
                weights = optimized_weights
            )

        return result


class MonteCarloSimulationOptimizer(PortfolioOptimizer):
    """ Simulates weights in order to maximize Sharpe Ratio and to minimize volatility 

    Args:
        PortfolioOptimizer ([type]): [description]
    """
    
    def _prepare_portfolio(self, df_portfolio) -> pd.DataFrame:
        raise NotImplementedError
    
    def _optimize_portfolio(self, df_portfolio) -> OptimizationResult:
        
        num_of_simulations = 3000
        
        # we need to store simulation results into arrays

        # prepare the weights array of numpy
        all_weights = np.zeros()


class SharpeRationOptimizer(PortfolioOptimizer):
    
    def _prepare_portfolio(self, df_portfolio) -> pd.DataFrame:
        raise NotImplementedError
    
    def _optimize_portfolio(self, df_portfolio) -> OptimizationResult:
        raise NotImplementedError