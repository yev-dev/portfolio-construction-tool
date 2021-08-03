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

</br>

<details>
<summary>Constraints Database Schema DLL</summary>
<br>
	CREATE SCHEMA IF NOT EXISTS pct AUTHORIZATION pct;

	
	create table rule_param_value (
        id integer generated by default as identity (start with 1),
        value varchar(50) not null,
        value_type varchar(25) not null,
        primary key (id)
    );
    
    
    create table rule_param_operation (
        id integer generated by default as identity (start with 1),
        operation varchar(25) not null,
        primary key (id)
    );

	
    create table constraint_rule_type (
        id integer generated by default as identity (start with 1),
        constraint_rule_type_name varchar(75) not null,
        constraint_rule_type_desc varchar(150) null,
        primary key (id)
    );
   
    create table constraint_rule (
        id integer generated by default as identity (start with 1),
        constraint_name varchar(75) not null,
        constraint_desc varchar(500) null,
        constraint_rule_type_id integer not null,
        parent_id integer null,
        primary key (id),
        foreign key(parent_id) references constraint_rule (id),
        foreign key(constraint_rule_type_id) references constraint_rule_type (id)
    );
    

    create table data_source_type (
        id integer generated by default as identity (start with 1),
        data_source_type_name varchar(75) not null,
        data_source_type_desc varchar(20) null,
        package_name varchar(150) null,
        target_class_name varchar(150) null,
        target_package_name varchar(150) null,
        primary key (id)
    );
    
    create table data_source (
        id integer generated by default as identity (start with 1),
        ext_source_id integer not null,
        data_source_name varchar(75) not null,
        data_source_type_id integer not null,
        primary key (id),
        foreign key(data_source_type_id) references data_source_type (id)
    );
	

   create table constraint_rule_param (
        constraint_rule_id integer not null,
        rule_param_operation_id integer not null,
        rule_param_value_id integer not null,
        primary key (constraint_rule_id, rule_param_operation_id, rule_param_value_id),
        foreign key(constraint_rule_id) references constraint_rule (id),
        foreign key(rule_param_operation_id) references rule_param_operation (id),
        foreign key(rule_param_value_id) references rule_param_value (id)
    );
    
    create table data_source_constraint_rule_param (
    	data_source_id integer not null,
    	constraint_rule_id integer not null,
        enable char(1) not null,
        primary key (data_source_id, constraint_rule_id ),
        foreign key(data_source_id) references data_source (id),
        foreign key(constraint_rule_id) references constraint_rule (id)
    );

	drop table if exists data_source_constraint_rule_param;
	drop table if exists constraint_rule_param;
	drop table if exists data_source_type;
	drop table if exists constraint_rule_type;
	drop table if exists rule_param_value;
	drop table if exists rule_param_operation;
	drop table if exists constraint_rule;
	drop table if exists data_source;


</details>