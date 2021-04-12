# Portfolio Constrution Tool

A simple implementation of portfolio construction tool with an optimizer exposed via Restful API.

The work is still in progress. Current implementation uses SciPy to optimize portfolio weights.

Jupyter notebook: [Portfolio Optimization](https://nbviewer.jupyter.org/github/yev-dev/portfolio-construction-tool/blob/main/notebooks/portfolio_optimization.ipynb)

![Portfolio Construction API](https://github.com/yev-dev/portfolio-construction-tool/blob/main/doc/portfolio-construction-api-swagger.png?raw=true)

### Installation with Conda or Pip

1. Python env setup

   Create conda environment from env file:

        conda env create -f environment.yml

    Alternatively, create create a virtual envrionment with 'venv'

        python3 -m venv env
        

2. Activate the environment:

        conda activate pct

        source env/bin/activate


3. Install pct in editable mode for active development

        pip install -e .

4. Install as a package

        pip install

5. If a new package is added to the requirements.txt file:
   

        pip install --upgrade -r requirements.txt

6. Removing installed virtual environment

    For conda:

        conda remove --name pct --all

    For pip env - delete associated directory


