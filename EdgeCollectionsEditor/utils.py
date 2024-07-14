import functools
import inspect
import json
import os.path
import pathlib
import shutil
import sqlite3
from subprocess import Popen
import typing

from EdgeCollectionsEditor.enums import *

T = typing.TypeVar("T")

def default_file_location()-> pathlib.Path:
    """ Returns the default location of the Edge Collections database file. """
    return (pathlib.Path(os.path.expandvars("$localappdata")) / "Microsoft/Edge/User Data/Default/Collections/collectionsSQLite").resolve()

def reveal_default_file_location():
    location = default_file_location()
    Popen(f'explorer /select,"{location}"')

def backup_database(file_location: pathlib.Path)-> pathlib.Path:
    """ Creates a backup of the Edge Collections database at the specified location. """
    i = 0
    newname = file_location.parent / f"{file_location.stem}_backup{i if i else ''}{file_location.suffix}"
    while newname.exists():
        i += 1
        newname = file_location.parent / f"{file_location.stem}_backup{i}{file_location.suffix}"
    shutil.copy(file_location, newname)
    return newname

def bytes_to_json(byteobj)-> str:
    """
    Utility function for converting bytes for json.dump/s(default=bytes_to_json).
    Various objects have blobs/bytes values that are not json serializable.

    Args:
        byteobj (bytes): The bytes to convert.

    Returns:
        str: The converted string.

    Raises:
        TypeError: If byteobj is not bytes.
    """
    if not isinstance(byteobj, bytes): raise TypeError("Must be bytes")
    return byteobj.decode("utf-8")

def convert_tag(collection_or_item: sqlite3.Row)-> dict[str, typing.Any]:
    """ Converts a collection or item's tag string to a dictionary and returns it.
        Note that this does not mutate the input.
    
    Args:
        collection_or_item (sqlite3.Row): The collection or item to convert.

    Returns:
        dict: The converted dictionary.
    """
    return json.loads(collection_or_item["tag"])

def _convert_byte_blob(key: str, object: str, returntype: typing.Type[T]=dict[str,str])-> typing.Callable[[sqlite3.Row],T]:
    """ This is a function factory for internal use. Used to create a funciton which converts a particular key's blob value to a dictionary and return it."""
    def convert(row: sqlite3.Row)-> returntype:
        f""" Converts the {key} of a {object} row to a dictionary and returns it.
            Note that this does not mutate the input.
        
        Args:
            row (sqlite3.Row): The row to convert.
        
        Returns:
            dict: The converted dictionary.
        """
        return json.loads(row[key], default = bytes_to_json)
    return convert

convert_thumbnail = _convert_byte_blob("thumbnail", "collection")
convert_canonical_image_data = _convert_byte_blob("canonical_image_data", "item")
convert_entity_blob = _convert_byte_blob("entity_blob", "item")
convert_source = _convert_byte_blob("source", "item")
convert_third_party_data = _convert_byte_blob("third_party_data", "item")

def truncate_blobs(*dicts: dict, trunc = 40, blobs = ["thumbnail", "canonical_image_data", "canonical_image_url", "entity_blob", "source", "third_party_data"])-> None:
    """ Truncates the specified blobs in the provided dicts.
    
    Args:
        *dicts (dict): The dicts to truncate.
        trunc (int, optional): The number of characters to truncate to.
        Defaults to 60. Note that an elipsis (...) will be appended to truncated values.
        blobs (list[str], optional): The blobs to truncate. Defaults to ["thumbnail", "canonical_image_data", "canonical_image_url", "entity_blob", "source", "third_party_data"].

    Raises:
        ValueError: If any of the dicts are not dicts.
    """
    for row in dicts:
        if not isinstance(row, dict): raise ValueError("All rows must be dicts.")
        for key in blobs:
            if key in row and (v:= row[key]):
                if len(v) <= trunc: continue
                if isinstance(v, bytes):
                    row[key] = v[:trunc]+b"..."
                else:
                    row[key] = v[:trunc]+"..."

def row_factory(func: typing.Callable[..., T])-> typing.Callable[..., T]:
    """
    Wraps a function so that the connection's row_factory is set to sqlite3.Row
        while the function is executed and restores it afterwards.
    """
    sig = inspect.signature(func)
    if "conn" not in sig.parameters:
        raise ValueError("The function must take a 'conn' parameter.")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        applied = sig.bind(*args, **kwargs)
        conn = applied.arguments["conn"]
        rf = conn.row_factory
        conn.row_factory = sqlite3.Row
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            conn.row_factory = rf
    return wrapper

class RowFactory:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.original = conn.row_factory
    def __enter__(self):
        self.original = self.conn.row_factory
        self.conn.row_factory = sqlite3.Row
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.row_factory = self.original

def rows_to_dict(*rows: sqlite3.Row)-> typing.Generator[dict, None, None]:
    """ Converts a list of sqlite3.Row objects to a list of dictionaries."""
    for row in rows:
        if not isinstance(row, sqlite3.Row):
            raise ValueError("All rows must be sqlite3.Row objects.")
        yield dict(row)

def sanitize_table_and_column(table: str, column: str)-> tuple[str, str]:
    """ Sanitizes a table and column name.
    
    Args:
        table (str): The table name.
        column (str): The column name.
    
    Returns:
        tuple[str, str]: The sanitized table and column names.

    Raises:
        KeyError: If the table or column name is invalid.
    """

    tableenum = Tables[table.upper()]

    match tableenum:
        case Tables.COLLECTIONS:
            return tableenum.value, Collections[column.upper()].value
        case Tables.ITEMS:
            return tableenum.value, Items[column.upper()].value
        case Tables.COLLECTIONS_SYNC:
            return tableenum.value, Collections_Sync[column.upper()].value
        case Tables.ITEMS_SYNC:
            return tableenum.value, Items_Sync[column.upper()].value
        case Tables.COLLECTIONS_ITEMS_RELATIONSHIP:
            return tableenum.value, Collections_Items_Relationship[column.upper()].value
        case Tables.FAVICONS:
            return tableenum.value, Favicons[column.upper()].value
        case Tables.META:
            return tableenum.value, Meta[column.upper()].value
        case Tables.COMMENTS:
            return tableenum.value, Comments[column.upper()].value
        case Tables.ITEMS_OFFLINE_DATA:
            return tableenum.value, Items_Offline_Data[column.upper()].value
        case Tables.COLLECTIONS_PRISM:
            return tableenum.value, Collections_Prism[column.upper()].value
        case _:
            ## Note: tableenum should trigger a KeyError when initialized if table is not in the Tables enum
            raise ValueError(f"Invalid table name: {table}")

