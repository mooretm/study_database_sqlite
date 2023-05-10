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
import tkinter as tk
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
        #print(f"dbmodel: Found {len(rows)} open studies")
        #for row in rows:
        #    print(row[0])
        return rows


    def select_all_studies(self, conn):
        print("\ndbmodel: Querying all studies...")
        cur = conn.cursor()
        cur.execute("SELECT Studies.study_id, Studies.irb_ref, Studies.study_name, Studies.study_type, Researchers.first_name || ' ' || Researchers.last_name AS [Full Name], Studies.date_created, Studies.date_closed FROM Studies INNER JOIN Researchers ON Studies.researcher_id = Researchers.researcher_id ORDER BY Studies.date_created DESC;")
        rows = cur.fetchall()
        #print(f"dbmodel: Found {len(rows)} total studies")
        return rows


    def select_active_researchers(self, conn):
        print("\ndbmodel: Querying active researchers...")
        cur = conn.cursor()
        cur.execute("SELECT first_name || ' ' || last_name AS [researcher_name], researcher_id FROM Researchers WHERE status='active'")
        rows = cur.fetchall()
        # print("dbmodel: Found the following researchers:")
        # for row in rows:
        #     print(row)
        return rows


    def update_study(self, conn, values):
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
