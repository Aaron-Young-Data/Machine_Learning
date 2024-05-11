import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
import pyodbc


class MySQLConnection:
    def __init__(self, port, database, user, password, server):
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.server = server

        self.connection_string = f'mysql+mysqlconnector://{user}:{password}@{server}:{port}/{database}'
        self.engine = create_engine(self.connection_string)
        self.conn = self.engine.connect()

        self.cursor_conn = mysql.connector.connect(
            user=user, password=password, host=server, database=database
        )

        self.cursor = self.cursor_conn.cursor()

    def run_query(self, query):
        try:
            df = pd.read_sql(query, self.conn)
            self.conn.close()
        except pyodbc.ProgrammingError as error:
            print(f'Warning: \n {error}')
        return df

    def run_query_no_output(self, query):
        try:
            self.cursor.execute(query)
            self.cursor.close()
            self.cursor_conn.close()
        except pyodbc.ProgrammingError as error:
            print(f'Warning: \n {error}')
        return None