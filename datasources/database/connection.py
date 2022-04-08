import os

from dotenv import load_dotenv

config = load_dotenv("../../.env")
DB_NAME = 'tickers'
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')

### Connect to the database ###
# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS/LOCALHOST>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}"\
    .format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
