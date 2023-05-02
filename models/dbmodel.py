""" Class for sqlite database.

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import database packages
import sqlite3
from sqlite3 import Error


#########
# BEGIN #
#########
class DBModel:
    """ Context manager for database connections. This ensures connecting and 
        disconnecting are always carried out without the user having 
        to remember.
    """
    def __init__(self):
        """ Define database path
        """
        pass


    #####################
    # General Functions #
    #####################
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn


    ###################
    # Query Functions #
    ###################
    def select_all_open_studies(self, conn):
        """
        Query all rows in the Studies table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT irb_reference, name, researcher_id, closure_date FROM Study WHERE closure_date IS NULL")

        rows = cur.fetchall()

        print("\ndbmodel: Querying all open studies...")
        print(f"dbmodel: Found {len(rows)} studies")
        for row in rows:
            print(row[0])

        return rows


    def select_all_open_studies2(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT S.irb_ref, S.study_name, R.first_name || ' ' || R.last_name AS [Full Name], S.date_created FROM Study AS S, Researcher AS R INNER JOIN Researcher ON S.researcher_id=R.researcher_id;")

        rows = cur.fetchall()

        return rows



