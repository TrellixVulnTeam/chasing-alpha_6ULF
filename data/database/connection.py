import os
import sys
import psycopg2

from dotenv import load_dotenv
from psycopg2 import OperationalError
from sqlalchemy import create_engine


config = load_dotenv("../../.env")
DB_NAME = 'tickers'
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS/LOCALHOST>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}"\
    .format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

def get_engine():
    return create_engine(DATABASE_URI)

# Adapted from https://medium.com/analytics-vidhya/part-4-pandas-dataframe-to-postgresql-using-python-8ffdb0323c09
def connect(db_name, db_user, db_password, db_host, db_port):
    """
    Responsible for handling database transactions.
    "autocommit" not set to true.
    Closing or destroying the connection will implicitly roll back the transaction
    :return: A connection to postgres via adapter psycopg2
    """
    conn = None
    try:
        print('Connecting to PostgreSQL...........')
        conn = psycopg2.connect(
            database=db_name, user=db_user, password=db_password, host=db_host, port=db_port
        )
        print("Connection successful..................")

    except OperationalError as err:
        show_psycopg2_exception(err)
        conn = None
    return conn


def show_psycopg2_exception(err):
    """
    Helper method for defining a function that handles and parses psycopg2 exceptions
    :param err: The error in which we are logging or printing
    :return: None
    """
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occurred
    line_n = traceback.tb_lineno
    print ("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
