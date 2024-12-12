# Wikimap

A map GUI for interacting with Wikipedia.

## Data

To setup the database from scratch, copy `config_example.json`, rename it to `config.json`, and change the parameters. The file used for the names list is found at https://www.kaggle.com/datasets/imoore/age-dataset. Change the `hard_reset` flag in `db_creation.py`, uncomment any of the query lines at the bottom of the file that are commented and run.

This will take a while as it must make many requests to a number of different APIs.

Alternatively load the preprocessed database from `database.db`.

## Application

To host the application. First import the database file `database_10_000.sql` to your local MySQL instance. Edit the `config.json` file to include the correct database name and other MySQL parameters. The remaining fields are not necessary for running the application.

To start the server, simply run `python3 main.py`, and navigate to http://127.0.0.1:8050/.