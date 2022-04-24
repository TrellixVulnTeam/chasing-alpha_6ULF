import psycopg2
from sqlalchemy.orm import sessionmaker
from io import StringIO
from data.database.connection import Connect, show_psycopg2_exception
from data.models.market_data_model import TickerPrice, Base

"""
Run CRUD operations against postgres db.
Reminder: always close the session to free up resources and connection.
Not closing a session will prevent you from recreating a database
"""

class Crud:

    def __init__(self, connect: Connect):
        self.connect = connect

    def get_session_maker(self):
        session_maker = sessionmaker(bind=self.connect.ENGINE)
        return session_maker()

    def insert_row(self, ticker_row_data: TickerPrice):
        with self.get_session_maker() as session:
            session.add(ticker_row_data)
            session.commit()

    def read_first_row(self):
        with self.get_session_maker() as session:
            row_data = session.query(TickerPrice).first()
            return row_data

    def recreate_database(self):
        """Drops all db create from 'Base' in models folder, then recreates them"""
        Base.metadata.drop_all(self.connect.ENGINE)
        Base.metadata.create_all(self.connect.ENGINE)

    def recreate_table_tickerprice(self):
        Base.metadata.drop(self.connect.ENGINE)
        Base.metadata.create(self.connect.ENGINE)

    # Define function using copy_from() with StringIO to insert the dataframe
    def copy_dataframe_to_database(self, conn, dataframe, table):
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
