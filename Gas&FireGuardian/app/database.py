import sqlite3
from sqlite3 import Error

DATABASE_PATH = '/Users/wangzhuohan/Desktop/Courseworks/year-3/semA/EE3070/Project/Gas&FireGuardian/app/sensor_data.db'  # Update this path accordingly


def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    """Create a table to store sensor data, without entry_id."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        field_number INTEGER,
        reading REAL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(f"An error occurred while creating the table: {e}")


def insert_reading(conn, timestamp, field_number, reading):
    """Insert a new reading into the sensor_data table."""
    insert_sql = """
    INSERT INTO sensor_data (timestamp, field_number, reading)
    VALUES (?, ?, ?);
    """
    try:
        c = conn.cursor()
        c.execute(insert_sql, (timestamp, field_number, reading))
        conn.commit()
    except Error as e:
        print(f"An error occurred while inserting data: {e}")


def retrieve_last_readings(conn, field_number, n):
    """Retrieve the last 'n' readings for a specific field, ordered by timestamp."""
    cursor = conn.cursor()
    cursor.execute("""
    SELECT reading FROM sensor_data 
    WHERE field_number = ? 
    ORDER BY datetime(timestamp) DESC LIMIT ?
    """, (field_number, n))
    rows = cursor.fetchall()
    return [reading[0] for reading in rows]
