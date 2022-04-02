import time

from sqlalchemy import create_engine
from datasources.database.market_data_model import Base

# TODO: capitalize const, create file for this, hide env vars
db_name = 'books'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'localhost'
db_port = '5432'

### Connect to the database ###
# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}"\
    .format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(DATABASE_URI)


def add_new_row(n):
    # Insert a new number into the 'numbers' table.
    db.execute("INSERT INTO numbers (number,timestamp) " + \
               "VALUES (" + \
               str(n) + "," + \
               str(int(round(time.time() * 1000))) + ");")


def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = "" + \
            "SELECT number " + \
            "FROM numbers " + \
            "WHERE timestamp >= (SELECT max(timestamp) FROM numbers)" + \
            "LIMIT 1"

    result_set = db.execute(query)
    for (r) in result_set:
        return r[0]

def recreate_database():
    Base.metadata.drop_all(db)
    Base.metadata.create_all(db)

if __name__ == '__main__':
    print('Application started')
    recreate_database()
    # while True:
    #     add_new_row(random.randint(1, 100000))
    #     print('The last value insterted is: {}'.format(get_last_row()))
    #     time.sleep(5)
