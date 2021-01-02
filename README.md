# Predictive MySQL Database Relationship Generator

## Requirements

- Python 3 +
- pip
- mysql-connector-python - pip package used to connect to mysql

## Installation

get started by installing mysql connector package using the following command

```sh
$ pip install mysql-connector-python
```

if you don't have pip in your path use the following command

```sh
$ python3 -m pip install mysql-connector-python
```

## Creating Pridictions File

To get the predicted relationships from a database use the python file `predictive.py`

```sh
$ python3 predictive.py -h localhost --db-prefix jugnoo -o tmp/predictions.json
```

to get help of the command line just use `python3 predictive.py --help`

## Generate Relationship Script

After generating a prediction file, the next step would be to generate a sql script to create the relationships inside the database.

Using the generated prediction json file's path in the below command you can generate a SQL script for altering the databases and tables to create the relationship

```sh
$ python3 gen-sql.py -h localhost -u root -p password --prediction tmp/predictions.json --output script.sql
```

# Contribution

Anyone who is eager in making this tool better and generic can fork and submit pull requrests.
