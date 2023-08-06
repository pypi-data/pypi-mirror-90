"""
flatlanddb.py - Loads the existing flatland database
"""
import sys
from pathlib import Path
from sqlalchemy import create_engine, MetaData
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def Create_relvars():
    """
    A relvar is a relational variable as defined by C.J. Date and Hugh Darwin.
    In the world of SQL it is effectively a table. Here we define all the relvars
    and then have the corresponding table schemas populated into the Sqlalchemy
    metadata.
    """
    from flatland.Database import relvars
    FlatlandDB.Relvars = relvars.define(FlatlandDB)
    FlatlandDB.MetaData.create_all(FlatlandDB.Engine)


def Populate():
    """
    Assign a value to each Flatland relvar. A value consists of a set of relations.
    In Sqlalchemy terms, the tables are all updated with initial row data.
    """
    # Iterate through the relvar dictionary to get each table
    print("Populating Flatland DB...")
    here = Path(__file__).parent
    pop_dirs = [
        here / "Connector", here / "Decorator", here / "Drawing", here / "Node",
    ]
    for d in pop_dirs:
        print(f"Appending dir: {d}")
        sys.path.append(str(d))

    for instances, relvar in FlatlandDB.Relvars.items():
        # Set i to the initial population of row values (set of relation values)
        i = __import__(instances + '_instances')  # Each population filename ends with '_instances.py'
        FlatlandDB.Connection.execute(relvar.insert(), i.population)  # Sqlalchemy populates the table schema


class FlatlandDB:
    """
    Flatland database containing all predefined Flatland data. We want to avoid having any predefined
    data declared in the code itself.

    Here we use Sqlalchemy to create the database engine and connection

        Attributes

        - File -- Local directory location of the sqlite3 database file
        - Metadata -- Sqlalchemy metadata
        - Connection -- Sqlalchemy database connection
        - Engine -- Sqlalchemy database engine
        - Relvars -- Dictionary of all relvar names and values (table names and row populations)
    """
    db_file_name = "Database/flatland.db"
    File = Path(__file__).parent.parent / db_file_name
    print(f'Flatalnd database file stored in: {str(File)}')
    MetaData = None
    Connection = None
    Engine = None
    Relvars = None

    def __init__(self, rebuild=True):
        """
        Create the sqlite3 database using Sqlalchemy

        :param rebuild: During development this will usually be true.  For deployment it should be false.
        """
        if rebuild:
            # Start with a fresh database
            if FlatlandDB.File.exists():
                FlatlandDB.File.unlink()

        db_path_str = str( FlatlandDB.File )
        FlatlandDB.Engine = create_engine(f'sqlite:///{db_path_str}', echo=True)
        FlatlandDB.Connection = FlatlandDB.Engine.connect()
        FlatlandDB.MetaData = MetaData(FlatlandDB.Engine)
        if rebuild:
            Create_relvars()
            Populate()
        else:
            # Just interrogate the existing database to get all the relvar/table names
            FlatlandDB.MetaData.reflect()


if __name__ == "__main__":
    #  Rebuild the database
    FlatlandDB()
