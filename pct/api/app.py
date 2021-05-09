import os
import logging
import sys
import connexion
from flask import jsonify

from pct.data.data_reader import SimpleIndexedCSVDataset
from pct.core.parameters import OptimizerParameters
from pct.core.optimizer import SimplePortfolioReturnOptimizer

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=logging.INFO, stream=sys.stdout)

DATA_DIR = os.getenv('DATA_DIR', os.path.join(os.path.expanduser('~'), r'Data/quant/prices'))
HISTORICAL_PRICES_5_YRS = os.path.join(DATA_DIR, 'prices_5yrs.csv')
HISTORICAL_PRICES_10_YRS = os.path.join(DATA_DIR, 'prices_10yrs.csv')


def status():
    return 'OK', 200

def tag():
    return 'scipy_optimizer_v1'

def metadata():
    return {"name" : tag()}

def optimize(body):

    request = connexion.request.get_json()
    tickers = request.get('tickers', None)

    if not tickers:
        return "Tickers are not found", connexion.status.HTTP_400_BAD_REQUEST

    parameters = OptimizerParameters(**request)

    # Should come from service and persistent storage
    pricing_service = SimpleIndexedCSVDataset(fpath=HISTORICAL_PRICES_5_YRS)
    df_prices = pricing_service.read()

    # Should come from instruments service with validation
    df_portfolio = df_prices[df_prices['ticker'].isin(tickers)]

    optimizer_service = SimplePortfolioReturnOptimizer(parameters)

    result = optimizer_service.optimize(df_portfolio=df_portfolio)

    return result

app = connexion.FlaskApp(__name__, specification_dir='./resources/')
app.add_api('pct.yml', arguments={'title': 'Portfolio Construction Api Service'}, pythonic_params=True)

# set the WSGI application callable to allow using uWSGI
# uwsgi --http :8080 -w app



if __name__ == '__main__':

    # Running with multi-threading support

    app.run(port=5000, use_reloader=False, threaded=True)

    # Running with multi-processes support
    # app.run(port=5000, use_reloader=False, threaded=False, processes=3)
    # Alternatively, you can run behind uWSGI server: i.e. gunicorn as we expose our application
    # app.run()


