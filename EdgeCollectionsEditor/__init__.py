import pathlib
import sqlite3

from EdgeCollectionsEditor.enums import *
from EdgeCollectionsEditor import utils
from EdgeCollectionsEditor.utils import row_factory

def connect_to_db(file_location: pathlib.Path|str|None = None)-> tuple[sqlite3.Connection, pathlib.Path]:
    """ Returns a connection to the Edge Collections database.
    
    If file_location is None, the default location will be used.
    """
    f = file_location

    if f is None:
        f = utils.default_file_location()
    elif not isinstance(f, pathlib.Path):
        f = pathlib.Path(f)

    if not f.exists():
        f = utils.default_file_location()
        if not f.exists():
            raise FileNotFoundError(f"Could not find Edge Collections database at {file_location}")
    if not f.is_file():
        raise ValueError(f"{file_location} is not a file")
    return sqlite3.connect(f), f

@row_factory
def check_syncable_collections(conn: sqlite3.Connection)-> list[sqlite3.Row]:
    """ Returns a list of collections that are syncable. """
    return conn.execute("""
SELECT collections_sync.*, collections.*
FROM collections
LEFT JOIN collections_sync ON collections.id = collections_sync.collection_id
WHERE collections_sync.is_syncable = 1 OR collections.is_syncable = 1;""").fetchall()

@row_factory
def get_table(conn: sqlite3.Connection, table_name: Tables)-> list[sqlite3.Row]:
    """ Returns a list of rows from the specified table. """
    if table_name not in Tables:
        raise ValueError(f"Invalid table name: {table_name}")
    return conn.execute(f"SELECT * FROM {table_name.value}").fetchall()

class ConnectionNamesRow(sqlite3.Row):
    id: str
    name: str
@row_factory
def list_collections(conn: sqlite3.Connection)-> list[ConnectionNamesRow]:
    """ Returns a list of collection titles and ids. """
    return conn.execute("SELECT id, title FROM collections").fetchall()

@row_factory
def get_collection_by_id(conn: sqlite3.Connection, collection_id: str)-> sqlite3.Row:
    """ Returns the collection with the specified id. """
    return conn.execute("SELECT * FROM collections WHERE id = ?", (collection_id,)).fetchone()

@row_factory
def get_collections_by_title(conn: sqlite3.Connection, collection_title: str)-> list[sqlite3.Row]:
    """ Returns a list of collections with the specified title. """
    return conn.execute("SELECT * FROM collections WHERE title = ?", (collection_title,)).fetchall()

@row_factory
def get_collections_by_title_like(conn: sqlite3.Connection, collection_title: str)-> list[sqlite3.Row]:
    """ Returns a list of collections with the specified title. """
    return conn.execute("SELECT * FROM collections WHERE title LIKE ?", (f"%{collection_title}%",)).fetchall()

def delete_collection(conn: sqlite3.Connection, collection_id: str):
    """ Deletes the collection with the specified id. """
    conn.execute("DELETE FROM collections WHERE id = ?", (collection_id,))

def edit_collection_title(conn: sqlite3.Connection, collection_id: str, title: str):
    """ Edits the title of the collection with the specified id. """
    conn.execute("UPDATE collections SET title = ? WHERE id = ?", (title, collection_id))

@row_factory
def list_items(conn: sqlite3.Connection)-> list[sqlite3.Row]:
    """ Returns a list of item titles and ids. """
    return conn.execute("SELECT id, title FROM items").fetchall()

@row_factory
def get_item_by_id(conn: sqlite3.Connection, item_id: str)-> sqlite3.Row:
    """ Returns the item with the specified id. """
    return conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

@row_factory
def get_items_by_title(conn: sqlite3.Connection, item_title: str)-> list[sqlite3.Row]:
    """ Returns a list of items with the specified title. """
    return conn.execute("SELECT * FROM items WHERE title = ?", (item_title,)).fetchall()

@row_factory
def get_items_by_title_like(conn: sqlite3.Connection, item_title: str)-> list[sqlite3.Row]:
    """ Returns a list of items with the specified title. """
    return conn.execute("SELECT * FROM items WHERE title LIKE ?", (f"%{item_title}%",)).fetchall()

@row_factory
def get_items_by_collection(conn: sqlite3.Connection, collection: str|sqlite3.Row)-> list[sqlite3.Row]:
    """ Returns a list of items in the specified collection.
    
    Args:
        conn (sqlite3.Connection): The connection to the Edge Collections database.
        collection (str|sqlite3.Row): The collection to get the items from.
            If a string is passed it will be used as the collection id.
    
    Returns:
        list[sqlite3.Row]: A list of items in the specified collection.
    """
    if isinstance(collection, sqlite3.Row):
        collection = collection["id"]
    return conn.execute("SELECT items.* FROM items LEFT JOIN collections_items_relationship ON items.id = collections_items_relationship.item_id WHERE parent_id = ?", (collection,)).fetchall()

@row_factory
def link_items_to_collections(conn: sqlite3.Connection, items: list[sqlite3.Row])-> list[dict]:
    """ Fetches the collections for each item provided and lists them under the nested keys "collections_items_relationships"->"parent_id".

    Args:
        conn (sqlite3.Connection): The connection to the Edge Collections database.
        items (list[sqlite3.Row]): A list of items to link to collections.

    Returns:
        list[dict]: A list of dictionaries containing the item and its connected collections, by way of collections_items_relationships key.
    """
    itemdicts = {item["id"]: item for item in utils.rows_to_dict(*items)}
    item_list = []
    for item in itemdicts.values():
        item['collections_items_relationships'] = []
        item_list.append(f'"{item['id']}"')
    connections = conn.execute(""" SELECT * FROM collections_items_relationship cir
                               LEFT JOIN collections c ON c.id = cir.parent_id
                               WHERE item_id IN (""" + ", ".join(item_list) + """)""").fetchall()
    for connection in connections:
        collection = list(utils.rows_to_dict(connection))[0]
        connection = {k: collection.pop(k) for k in ["item_id", "parent_id", "position"]}
        connection['parentid'] = collection
        item = itemdicts[connection['item_id']]
        item['collections_items_relationships'].append(connection)
    return list(itemdicts.values())