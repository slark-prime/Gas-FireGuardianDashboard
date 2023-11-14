import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from database import create_connection, create_table, insert_reading

THINGSPEAK_API_URL = "https://api.thingspeak.com/channels/2288043/feeds.json?api_key=P2RLVV3MD96KYZB6&results=2"

def retrieve_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def simulate_data_fetching():
    timestamp = datetime.now()
    # Simulate 12 readings for each field, separated by spaces
    field1_readings = ' '.join(f"{np.random.uniform(20, 30):.2f}" for _ in range(12))
    field2_readings = ' '.join(f"{np.random.uniform(30, 50):.2f}" for _ in range(12))
    field3_readings = ' '.join(f"{np.random.uniform(0, 1):.2f}" for _ in range(12))
    # ... You can add more field simulations as necessary ...

    simulated_json_data = {
        "feeds": [{
            "entry_id": np.random.randint(100, 999),
            "created_at": timestamp.isoformat(),  # Convert to ISO format string
            "field1": field1_readings,
            "field2": field2_readings,
            "field3": field3_readings,
            # "field4": None,  # Include this if you want to simulate a 'null' field
        }]
    }
    # print(f"Generated simulated data: {simulated_json_data}")

    return simulated_json_data


def distribute_timestamps_within_span(end_timestamp, span_seconds, count):
    """Generate evenly spaced timestamps within a span leading up to the end timestamp."""
    end_time = datetime.fromisoformat(end_timestamp.replace('Z', '+00:00'))
    if count > 1:
        interval_seconds = span_seconds / (count - 1)
    else:
        interval_seconds = 0  # if count is 1, there are no gaps to calculate
    return [(end_time - timedelta(seconds=interval_seconds * i)).isoformat() for i in range(count)][::-1]


def process_and_store_last_feed_data(conn, feed_data):
    """Process and store only the last feed data into the database if it's newer than the latest entry."""
    last_feed = feed_data['feeds'][-1]
    final_timestamp = last_feed.get("created_at")

    # Check the latest timestamp in the database
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(timestamp) FROM sensor_data")
    result = cursor.fetchone()

    # If there are no previous entries in the database, result will be (None,)
    latest_timestamp = result[0] if result[0] is not None else None
    timezone_offset = 8
    # If there's no previous entry or the new timestamp is more recent, insert the new data
    if latest_timestamp is None or final_timestamp > latest_timestamp:
        for i in range(1, 6):  # Including field5 based on the provided data
            field_key = f"field{i}"
            readings = last_feed.get(field_key)
            if readings:
                # Split by space and filter out any empty strings
                readings_list = [r for r in readings.split(' ') if r]
                # Calculate timestamps for each reading
                timestamps = distribute_timestamps_within_span(final_timestamp, 15, len(readings_list))

                print(timestamps)
                # Insert each reading into the database with the corresponding timestamp
                for reading, timestamp in zip(readings_list, timestamps):
                    try:
                        insert_reading(conn, timestamp, i, float(reading))
                    except ValueError as e:
                        print(f"An error occurred while inserting data: {e}")
        conn.commit()  # Commit the transaction if insert_reading doesn't do it
        return True  # Indicate that new data was inserted
    else:
        return False  # Indicate no new data was inserted


def get_data_for_plotting(conn, field_number, n_points):
    try:
        print(f"Fetching {n_points} points for field {field_number}")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT timestamp, reading FROM sensor_data 
        WHERE field_number = ? 
        ORDER BY timestamp DESC LIMIT ?
        """, (field_number, n_points))
        results = cursor.fetchall()
        cursor.close()  # Explicitly close the cursor

        print(f"Fetched {len(results)} points")  # Log the actual number of points fetched

        if not results:
            print("No results found.")
            return {'timestamps': [], 'readings': [], 'average_values': []}

        timestamps, readings = zip(*results)  # Separates the results into timestamps and readings

        # Convert timestamps to proper ISO 8601 format and reverse order
        formatted_timestamps = [datetime.fromisoformat(ts.replace('Z', '+00:00')).isoformat() for ts in reversed(timestamps)]

        # Reverse the readings to match timestamps and calculate average
        reversed_readings = list(reversed(readings))
        average_value = np.mean(reversed_readings) if reversed_readings else None
        average_values = [average_value] * len(reversed_readings) if average_value is not None else []

        data_for_frontend = {
            'timestamps': formatted_timestamps,
            'readings': reversed_readings,
            'average_values': average_values
        }

        return data_for_frontend
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'timestamps': [], 'readings': [], 'average_values': []}


if __name__ == "__main__":
    conn = create_connection()
    create_table(conn)
    api_data = retrieve_data(THINGSPEAK_API_URL)
    # Process only the last feed from the simulated API data
    process_and_store_last_feed_data(conn, api_data)

    conn.close()
