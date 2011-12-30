# coding=utf-8

"A small wrapper for the PyPKM SQLite database."

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import os
import sqlite3

this_dir = os.path.dirname(os.path.abspath(__file__))

def get_cursor():
    "Return a SQLite cursor for queries."
    conn = sqlite3.connect(os.path.join(this_dir, 'pypkm.sqlite'))
    
    return conn.cursor()