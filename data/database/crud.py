import psycopg2
from sqlalchemy.orm import sessionmaker
from io import StringIO
from data.database.connection import get_engine, show_psycopg2_exception
from data.models.market_data_model import TickerPrice, Base

"""
Run CRUD operations against postgres db.
Reminder: always close the session to free up resources and connection.
Not closing a session will prevent you from recreating a database
"""

def get_session_maker():
    session_maker = sessionmaker(bind=get_engine())
    return session_maker()

def insert_row(ticker_row_data: TickerPrice):
    with get_session_maker() as session:
        session.add(ticker_row_data)
        session.commit()

def read_first_row():
    with get_session_maker() as session:
        row_data = session.query(TickerPrice).first()
        return row_data

def recreate_database():
    """Drops all db create from 'Base' in models folder, then recreates them"""
    Base.metadata.drop_all(get_engine())
    Base.metadata.create_all(get_engine())

# Define function using copy_from() with StringIO to insert the dataframe
def copy_dataframe_to_database(conn, dataframe, table):
    """
    :param conn:
    :param dataframe: copy this dataframe to the database
    :param table: table name as a string
    :return:
    """
    # save dataframe to an in memory buffer
    buffer = StringIO()
    dataframe.to_csv(buffer, header=False, index=True)
    buffer.seek(0)
    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep=",")
        print("Data inserted using copy_from_datafile_StringIO() successful....")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as err:
        # pass exception to function
        show_psycopg2_exception(err)
        conn.rollback()
    finally:
        cursor.close()
