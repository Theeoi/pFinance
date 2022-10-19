#!/usr/bin/env python
"""
Main source file of pfinance.
"""
import argparse
import os
import sqlite3

import pandas as pd

DATABASE = 'database/database.db'
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
        return sqlite3.connect(self.path)

    def check_db(self) -> bool:
        """
        Check if database file exists.
        Returns True if it exists.
        """
        return os.path.exists(self.path)

    def read_database(self) -> dict[str, pd.DataFrame | None]:
        """
        Returns database entries in {table} as a DataFrame.
        If database is empty or does not exist return None.
        """
        df_dict = {}

        query_tables = """
        SELECT name FROM sqlite_master WHERE type='table';
        """
        self.curr.execute(query_tables)
        tables = [v[0] for v in self.curr.fetchall() if v[0] !=
                  "sqlite_sequence"]
        for table in tables:
            try:
                df_dict[table] = pd.read_sql(f"""SELECT * FROM {table}""",
                                             self.conn,
                                             index_col=[
                                                 'Transaction date', 'Category'
                                             ],
                                             parse_dates=['Transaction date'])
            except KeyError:
                df_dict[table] = None
            except pd.errors.DatabaseError:
                df_dict[table] = None

        return df_dict

    def load_to_database(self, table: str, xl_path: str) -> None:
        """
        Read excel-file into database table.
        Appends new entries through replacing old matching ones.
        """
        input_data = pd.read_excel(xl_path, header=5, usecols='C,E,G,I',
                                   parse_dates=[0])
        input_data['Category'] = 'Övrigt'
        # Set category for each expense here!
        input_data = input_data.set_index(['Transaction date', 'Category'])

        current_db: dict[str, pd.DataFrame | None] = self.read_database()
        if table not in current_db or current_db[table] is None:
            agg_data: pd.DataFrame = input_data
        else:
            agg_data = current_db[table].combine_first(input_data)
            agg_data.drop_duplicates(inplace=True)

        agg_data.sort_index(level='Transaction date', inplace=True,
                            ascending=False)

        agg_data.to_sql(name=table, con=self.conn, schema=DB_SCHEMA,
                        if_exists='replace', index=True,
                        index_label=['Transaction date', 'Category'])
        self.conn.commit()


def get_cliargs() -> dict:
    """
    Captures cli input and returns a dictionary of the input.
    Modify this function to add additional arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--show", action='store_true',
                        help="Shows the current data in database.")

    parser.add_argument("-l", "--load", type=str, nargs=2,
                        metavar=("table_name", "file_path"),
                        default=None,
                        help="""
                        Loads the specified .ods file to specified table in sql database.
                        """)

    return vars(parser.parse_args())


def main():
    """
    Entrypoint to module.
    """
    db = Database(DATABASE)

    args: dict = get_cliargs()

    if args['show'] is not False:
        print(f"Current database:\n{db.read_database()}")

    if args['load'] is not None:
        table_name = args['load'][0]
        file_path = args['load'][1]
        if not os.path.exists(file_path):
            raise ValueError(f"""
                    ValueError: Invalid file path/name. Path {file_path}
                    does not exist.
                    """)
        if not file_path.endswith('.ods'):
            raise ValueError(f"""
                    ValueError: Invalid file format. {file_path} must be a
                    .ods file.
                    """)
        db.load_to_database(table_name, file_path)

    # Closing all active databases
    for db_instance in Database.instances:
        db_instance.conn.close()


if __name__ == "__main__":
    main()
