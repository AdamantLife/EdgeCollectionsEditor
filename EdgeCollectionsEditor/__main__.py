import argparse
import pathlib
from pprint import pprint
import sqlite3

import EdgeCollectionsEditor as ECE
from EdgeCollectionsEditor import utils

def query_table(db: sqlite3.Connection, table: ECE.Tables, column: str, value: str, like: bool = False)-> list[sqlite3.Row]:
    """ Queries the specified table for the specified column and value. """
    tablename, columnname = utils.sanitize_table_and_column(table.value, column)
    if like:
        with utils.RowFactory(db):
            return db.execute(f'SELECT * FROM {tablename} WHERE {columnname} LIKE ?;', (f"%{value}%",)).fetchall()
    with utils.RowFactory(db):
        return db.execute(f"SELECT * FROM {tablename} WHERE {columnname} = ?;", (value,)).fetchall()

def sample_data(args: argparse.Namespace):
    """ Prints sample data from the Edge Collections database. """
    db, _ = ECE.connect_to_db(file_location=args.file_location)
    limit = 1
    if args.limit is not None:
        limit = args.limit
    if args.column is not None:
        if not args.value or not args.table:
            raise ValueError("Both --value and --table must be specified to filter the sample data.")
        results = query_table(db, args.table, args.column, args.value, like=args.like)
    elif args.table is not None:
        results = ECE.get_table(db, args.table)
    else:
        for table in ECE.Tables:
            result = ECE.get_table(db, table)
            print(table, len(result))
            results = list(utils.rows_to_dict(*result[:limit]))
            utils.truncate_blobs(*results)
            pprint(results)
            print("-----\n")
        return
    print(len(results))
    results = list(utils.rows_to_dict(*results[:limit]))
    utils.truncate_blobs(*results)
    pprint(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file_location", type=pathlib.Path, default=None)
    parser.add_argument("-t", "--table", type=ECE.Tables, default=None)
    parser.add_argument("-l", "--limit", type=int, default=None)
    parser.add_argument("-c", "--column", type=str, default=None)
    parser.add_argument("-v", "--value", type=str, default=None)
    parser.add_argument("--like", action="store_true", default=False)
    parser.set_defaults(func=sample_data)

    args = parser.parse_args()

    args.func(args)