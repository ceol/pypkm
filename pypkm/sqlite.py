import os
import sqlite3

this_dir = os.path.dirname(os.path.abspath(__file__))

def get_cursor(self):
    "Return a SQLite cursor for queries."
    conn = sqlite3.connect(os.path.join(self.this_dir, 'pypkm.sqlite'))
    
    return conn.cursor()