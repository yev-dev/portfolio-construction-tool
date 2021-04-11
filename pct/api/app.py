import logging
import sys
import connexion

from connexion.resolver import RestyResolver

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=logging.INFO, stream=sys.stdout)


def status():
    return 'OK', 200

def tag():
    return 'scipy_optimizer_v1'

def metadata():
    return {"name" : tag()}

def optimize(**kwargs):
    return {}



app = connexion.FlaskApp(__name__, specification_dir='./resources/')
app.add_api('pct.yml')

# app.add_api('pct.yml', resolver=RestyResolver('pct.api'), arguments={'title': 'Portfolio Construction Api Service'}, pythonic_params=True)

# set the WSGI application callable to allow using uWSGI
# uwsgi --http :8080 -w app

application = app.app

if __name__ == '__main__':

    # Running with multi-threading support

    app.run(port=5000, use_reloader=False, threaded=True)

    # Running with multi-processes support
    # app.run(port=5000, use_reloader=False, threaded=False, processes=3)
    # Alternatively, you can run behind uWSGI server: i.e. gunicorn as we expose our application
    # app.run()


