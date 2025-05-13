# db_inspect.py

import sqlite3
from pprint import pprint

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("=== documents ===")
cursor.execute("SELECT * FROM documents;")
pprint(cursor.fetchall())

print("\n=== thumbnails ===")
cursor.execute("SELECT * FROM thumbnails;")
pprint(cursor.fetchall())

print("\n=== conflicts ===")
cursor.execute("SELECT * FROM conflicts;")
pprint(cursor.fetchall())

conn.close()
