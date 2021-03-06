
from unittest import TestCase
from typing import List

from pct.core.parameters import OptimizerParameters
from pct.util.exceptions import OptimizationFunctionException, OptimizationParametersException
from pct.util.util import print_dictionary


class TestOptimizationParameterFunctions(TestCase):

    def test_can_extract_function_by_key(self):
        instruments = ['AAPL', 'VOD']
        function = OptimizerParameters.get_function(
            OptimizerParameters.EQUALLY_WEIGHTED_FUNC)
        self.assertEqual([0.5, 0.5], function(instruments))

    def test_function_exception_thrown_when_function_not_found(self):
        self.assertRaises(OptimizationFunctionException, OptimizerParameters.get_function('wrong_function'))

    def test_optimizer_dummy_function(self):

        list_of_constraints = {
            'dummy': 'eq'
        }

        constraints = []

        for function, operation in list_of_constraints.items():
            constraint = {}
            constraint['type'] = operation
            constraint['fun'] = OptimizerParameters.get_function(function)
            constraints.append(constraint)

        self.assertTrue(len(constraints) == 1)

        extracted_dummy_func = constraints[0]['fun']

        return_value = extracted_dummy_func(2)

        self.assertTrue(
            "Check if dummy loopback function extracted from registry give us same value", return_value == 2)

        constraints = tuple(constraints)
        self.assertIsNotNone(constraints)

    def test_multiple_functions(self):

        list_of_constraints = [
            {
              'function' : "sum_of_weights",
              'operation' : "eq"
            },
            {
              'function' : "target_return",
              'operation' : "eq"
            },
        ]

        constraints = []

        for constraint  in list_of_constraints:
            _constraint = {}
            _constraint['type'] = constraint['operation']
            _constraint['fun'] = OptimizerParameters.get_function(constraint['function'])
            constraints.append(_constraint)
        
        # constraints_2 = [ {k : v} for constraint in list_of_constraints for k,v in zip(['fun', 'type'], [ v for k,v in constraint.items() ] ) ]
        
        self.assertTrue(len(constraints) == 2)

    def test_optimizer_parameters_transformation(self):

        parameters = build_sample_optimization_parameters()
        transformed_params = parameters.params
        self.assertEquals(transformed_params[OptimizerParameters.METHOD_KEY], 'SLSQP')
        self.assertEquals(transformed_params[OptimizerParameters.TICKERS_KEY], ['APPL', 'FB'])
        self.assertEquals(transformed_params[OptimizerParameters.INITIAL_WEIGHTS_KEY], [0.5, 0.5])

        print("---------------------Transformed Parameters---------------")
        # print_dictionary(transformed_params)
    

    def test_expected_error_without_mandatory_parameters(self):
        
        with self.assertRaises(OptimizationParametersException) as context:
            parameters = OptimizerParameters(**{})
    
    def test_expected_error_with_wrong_parameters(self):
        request = {}
        request['wrong_key'] = 'wrong_value'
        
        with self.assertRaises(OptimizationParametersException) as context:
            parameters = OptimizerParameters(**request)

def build_sample_optimization_parameters(tickers: List = None, constraints: List = None):

    tickers = ['APPL', 'FB'] if not tickers else tickers

    if not constraints:
        constraints = [
            {
              'function' : "sum_of_weights",
              'operation' : "eq"
            }
        ]
        
    request = {}
    request[OptimizerParameters.TAG_KEY] = 'scipy_optimizer_v1'
    request[OptimizerParameters.TICKERS_KEY] = tickers
    request[OptimizerParameters.FUNCTION_KEY] = OptimizerParameters.PORTFOLIO_RETURN_FUNC
    request[OptimizerParameters.CONSTRAINTS_KEY] = constraints

    return OptimizerParameters(**request)