import logging
import numpy as np
import pandas as pd

from collections import defaultdict
from pct.util.exceptions import OptimizationFunctionException, OptimizationParametersException


logger = logging.getLogger(__name__)


class OptimizerParameters(object):
    """
    Holds options than can be used to configure portfolio optimization.
    Currently doesn't do much but can be extended for saving metadata/reproducibility

    """
    TAG_KEY = 'tag'

    FUNCTION_KEY = 'func'
    CONSTRAINTS_KEY = 'constraints'
    INITIAL_WEIGHTS_KEY = 'initial_weights'
    TICKERS_KEY = 'tickers'
    METHOD_KEY = 'method'
    BOUNDS_KEY = 'bounds'

    EQUALLY_WEIGHTED_FUNC = 'equally_weighted'
    SUM_OF_WEIGHTS_FUNC = 'sum_of_weights'
    TARGET_RETURN_FUNC = 'target_return'
    PORTFOLIO_RETURN_FUNC = 'portfolio_return'

    def __init__(self, **optimizer_params):
        """
        Constructor for optimizer config class
        param optimizer_params: kwargs - options for signal generator
        """
        self._params = self._transform_parameters(**optimizer_params)
    
    @property
    def params(self):
        return self._params

    def _transform_parameters(self, **optimizer_params):

        logger.info("Transforming optimization parameters")

        # Helper method to wrap lambda exception
        def raise_(ex):
            raise ex

        parameters = defaultdict(lambda: raise_(
            OptimizationParametersException('Requested function does not exist')))

        try:
            # Mandatory constraints.
            # We expect to exit the programs if mandatory keys are not provided

            tickers = optimizer_params[OptimizerParameters.TICKERS_KEY]

            func = self.get_function(optimizer_params[OptimizerParameters.FUNCTION_KEY])

            initial_weights = optimizer_params.get(OptimizerParameters.INITIAL_WEIGHTS_KEY, None)

            if not initial_weights:
                initial_weights_func = self.get_function(OptimizerParameters.EQUALLY_WEIGHTED_FUNC)
                initial_weights = initial_weights_func(tickers=tickers)

            bounds = tuple((0, 1) for ticker in range(len(tickers)))

            method = optimizer_params.get(OptimizerParameters.METHOD_KEY, 'SLSQP')

            # Constraints come in a form of function names {'type': 'eq', 'fun': sum_of_weights }

            constraints = []

            for _function, _operation in optimizer_params[OptimizerParameters.CONSTRAINTS_KEY].items():
                _constraint = {}
                _constraint['type'] = _operation
                _constraint['fun'] = OptimizerParameters.get_function(_function)
                constraints.append(_constraint)

            if not constraints:
                raise OptimizationParametersException(f"No constraints provided")

        except (KeyError, NameError, OptimizationFunctionException) as e:
            logger.error(f"Failed to extract parameter keys: {e}")
            raise OptimizationParametersException(e) from e
        else:
            parameters[OptimizerParameters.METHOD_KEY] = method
            parameters[OptimizerParameters.TICKERS_KEY] = tickers
            parameters[OptimizerParameters.FUNCTION_KEY] = func
            parameters[OptimizerParameters.INITIAL_WEIGHTS_KEY] = initial_weights
            parameters[OptimizerParameters.BOUNDS_KEY] = bounds
            parameters[OptimizerParameters.CONSTRAINTS_KEY] = constraints
            return parameters


    def __str__(self):
        return self.__repr__()

    def __repr__(self):

        attrs_list = ["{}={!r}".format(attr_name, getattr(self, attr_name))
                      for attr_name in self._attributes
                      if getattr(self, attr_name) is not None]

        attrs = ", ".join(attrs_list)
        cls_name = self, __class__.__name__
        return "{}({})".format(cls_name, attrs)

    @staticmethod
    def get_function(function_key: str):
        """Extract lambda function from registry by key.

        Args:
            function_key (str): function name.
        :raises:
            OptimizationFunctionException: if function can't be found.
        """

        # Helper method to wrap lambda exception
        def raise_(ex):
            raise ex

        # Methods related to optimisation functions

        def portfolio_returns(weights, df_portfolio):
            # Distribute allocation by weights
            df_portfolio = df_portfolio * weights
            portfolio_return = df_portfolio.sum(axis=1)
            portfolio_return = portfolio_return[-1]

            # Minimum is a maximum, we need to negate as SciPy optimizer can only minimize
            return -portfolio_return

        # Defining all function in function_mapper registry

        functions_mapper = defaultdict(lambda: raise_(
            OptimizationFunctionException('Requested function does not exist')))

        functions_mapper = {
            'dummy': lambda x: x,
            'equally_weighted': lambda tickers: len(tickers) * [1 / len(tickers)],
            'sum_of_weights': lambda weights: np.sum(weights) - 1.0,
            'target_return': lambda weights, target_return, expected_returns: target_return - weights.T@expected_returns,
            'portfolio_return': portfolio_returns
        }

        return functions_mapper.get(function_key)
