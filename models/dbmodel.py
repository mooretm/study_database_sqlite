""" Class for sqlite database.

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import database packages
import sqlite3
from sqlite3 import Error

# Import GUI packages
from tkinter import messagebox


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
    def get_studyid_from_name(self, conn, study_name):
        """ Get the study_id for the provided study name.
        """
        print("\ndbmodel: Querying study id...")
        cur = conn.cursor()
        sql = '''SELECT study_id FROM Studies WHERE study_name=?'''
        cur.execute(sql, study_name)
        rows = cur.fetchall()
        print(f"dbmodel: {study_name[0]} ID: {rows[0][0]}")
        return rows


    def select_open_studies(self, conn):
        """
        Query all rows in the Studies table
        :param conn: the Connection object
        :return:
        """
        print("\ndbmodel: Querying open studies...")
        cur = conn.cursor()
        cur.execute("SELECT Studies.study_id, Studies.irb_ref, Studies.study_name, Studies.study_type, Researchers.first_name || ' ' || Researchers.last_name AS [Full Name], Studies.date_created, Studies.date_closed FROM Studies INNER JOIN Researchers ON Studies.researcher_id = Researchers.researcher_id WHERE Studies.date_closed IS NULL ORDER BY Studies.date_created DESC;")
        rows = cur.fetchall()
        print(f"dbmodel: Found {len(rows)} open studies")
        return rows


    def select_all_studies(self, conn):
        """ Select all studies.
        """
        print("\ndbmodel: Querying all studies...")
        cur = conn.cursor()
        cur.execute("SELECT Studies.study_id, Studies.irb_ref, Studies.study_name, Studies.study_type, Researchers.first_name || ' ' || Researchers.last_name AS [Full Name], Studies.date_created, Studies.date_closed FROM Studies INNER JOIN Researchers ON Studies.researcher_id = Researchers.researcher_id ORDER BY Studies.date_created DESC;")
        rows = cur.fetchall()
        print(f"dbmodel: Found {len(rows)} total studies")
        return rows


    def select_active_researchers(self, conn):
        """ Select all active researchers.
        """
        print("\ndbmodel: Querying active researchers...")
        cur = conn.cursor()
        cur.execute("SELECT first_name || ' ' || last_name AS [researcher_name], researcher_id FROM Researchers WHERE status='active'")
        rows = cur.fetchall()
        print(f"dbmodel: Found {len(rows)} active researchers")
        return rows


    def select_amendments(self, conn, study_id):
        """ Select all amendments for a given study id.
        """
        print("\ndbmodel: Querying amendments...")
        cur = conn.cursor()
        sql = '''SELECT * FROM Amendments WHERE study_id=?'''
        cur.execute(sql, study_id)
        rows = cur.fetchall()
        print(f"dbmodel: Found {len(rows)} amendments")
        return rows


    def update_study(self, conn, values):
        """ Update details in Studies table.
        """
        print(f"\ndbmodel: Updating study record: {values[6]}...")
        sql = '''UPDATE Studies SET irb_ref=?, study_name=?, study_type=?, researcher_id=?, date_created=?, date_closed=? WHERE study_id=?'''
        cur = conn.cursor()
        try:
            cur.execute(sql, values)
            conn.commit()
            print("dbmodel: Done!")
        except sqlite3.IntegrityError as e:
            print(f"dbmodel: {e}")
            messagebox.showerror(
                title="Request Failed",
                message="Could not complete request!",
                detail=f"{e}"
            )


    def create_study(self, conn, values):
        """ Add a new study to the Studies table.
        """
        print(f"\ndbmodel: Creating new study record...")
        sql = '''INSERT INTO Studies(irb_ref, study_name, study_type, researcher_id, date_created, date_closed) VALUES(?,?,?,?,?,?)'''
        cur = conn.cursor()
        try:
            cur.execute(sql, values)
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"dbmodel: {e}")
            messagebox.showerror(
                title="Request Failed",
                message="Could not complete request!",
                detail=f"{e}"
            )
