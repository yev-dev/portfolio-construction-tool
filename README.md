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

### OpenAPI client generation 

Portfolio Construction Tool exposes operations via Restful API endpoints and OpenAPI specification for stronly typed server/client.

Get the latest version of swagger-codegen from [swagger-codegen git repository](https://github.com/swagger-api/swagger-codegen) or install it with brew command:

        brew install swagger-codegen



## Constraints Database setup
</br>


        psql postgres -U admin
        
        CREATE DATABASE pct;
        create user pct with encrypted password 'password123';
        ALTER ROLE pct CREATEDB;

        # Granting permissions to create schema
        GRANT CREATE ON DATABASE pct to pct;

#### Database Schama Design
</br>

![Portfolio Construction API](https://github.com/yev-dev/portfolio-construction-tool/blob/main/doc/constraints-db-schema.png?raw=true)