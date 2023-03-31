import sqlite3

def __connect_to_db():
    conn = sqlite3.connect('shrtly.db');
    print(conn)
    conn.row_factory = sqlite3.Row
    return conn