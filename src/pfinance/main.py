#!/usr/bin/env python
"""
Main source file of pfinance.
"""
import sqlite3
import os
import pandas as pd

CARD_DB = 'database/card.db'
DB_SCHEMA = 'database/schema.sql'


class Database:
    """
    Class for sqlite database for storage of financial data.
    """
    instances: list = []

    def __init__(self, path: str) -> None:
        self.path = path
        self.conn = self.create_connection()
        self.curr = self.conn.cursor()

        Database.instances.append(self)

    def __repr__(self) -> str:
        return f"Database({self.path})"

    def create_connection(self) -> sqlite3.Connection:
        """
        Return a connection to the database. Create a new database if is does
        not exist.
        """
        if not self.check_db():
            # If database not exist -> Create with template
            print("Creating new database")
            with open(DB_SCHEMA, 'r', encoding='utf8') as schema_template:
                schema = schema_template.read()
                conn = sqlite3.connect(self.path)
                conn.executescript(schema)
        else:  # Else simply create the connection
            conn = sqlite3.connect(self.path)

        return conn

    def check_db(self) -> bool:
        """
        Check if database file exists.
        """
        return os.path.exists(self.path)

    def read_database(self) -> pd.DataFrame:
        """
        Returns database entries as a DataFrame.
        """
        return pd.read_sql("""
                SELECT * FROM ledger
                """, self.conn, index_col=['Transaction date', 'Category'],
                           parse_dates=['Transaction date'])

    def load_to_database(self, xl_path: str) -> None:
        """
        Read excel-file into database table.
        Appends new entries through replacing old matching ones.
        """
        new_data = pd.read_excel(xl_path, header=5, usecols='C,E,G,I',
                                 parse_dates=[0])
        new_data['Category'] = 'Övrigt'
        # Set category for each expense here!
        new_data = new_data.set_index(['Transaction date', 'Category'])

        new_data.to_sql(name="ledger", con=self.conn, schema=DB_SCHEMA,
                        if_exists='replace', index=True,
                        index_label=['Transaction date', 'Category'])
        self.conn.commit()


def main():
    """
    Entrypoint to module.
    """
    carddata = Database(CARD_DB)
    print(carddata)

    # carddata.load_to_database(
    #     "/home/theodorb/Downloads/kontotransactionlist.ods")

    print(carddata.read_database())

    # Closing all active databases
    for db_instance in Database.instances:
        db_instance.conn.close()


if __name__ == "__main__":
    main()
