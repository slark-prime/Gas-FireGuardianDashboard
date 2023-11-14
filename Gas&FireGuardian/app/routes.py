from app import app, scheduler
from flask import render_template, jsonify, send_from_directory
from .data_fetcher import get_data_for_plotting, retrieve_data, process_and_store_last_feed_data, simulate_data_fetching
from database import create_connection

THINGSPEAK_API_URL = "https://api.thingspeak.com/channels/2288043/feeds.json?api_key=P2RLVV3MD96KYZB6&results=2"


def update_sensor_data():
    """Fetch data from ThingSpeak and update the database if new data is available."""
    # Fetch data from ThingSpeak
    feed_data = retrieve_data(THINGSPEAK_API_URL)
    # feed_data = simulate_data_fetching()
    # Process and store the last feed data into the database if it's newer
    conn = create_connection()
    new_data_inserted = False
    if feed_data:
        new_data_inserted = process_and_store_last_feed_data(conn, feed_data)
    conn.close()

    return new_data_inserted


# Define the scheduled task
@scheduler.task('interval', id='update_data_task', seconds=15, misfire_grace_time=900)
def scheduled_update_data():
    if update_sensor_data():
        print("New data was fetched from ThingSpeak and updated to the database.")
    else:
        print("No new data to update or data is not newer than the latest entry.")



@app.route('/')
def index():
    # Render the main dashboard page.
    return render_template('index.html')


@app.route('/update_data', methods=['POST'])
def update_data():
    # Fetch data from ThingSpeak
    # feed_data = fetch_data_from_thingspeak(THINGSPEAK_API_URL)
    feed_data = simulate_data_fetching()
    # Process and store the last feed data into the database
    conn = create_connection()
    updated = False
    if feed_data:
        updated = process_and_store_last_feed_data(conn, feed_data)
    conn.close()

    if updated:
        return jsonify({"success": True, "message": "Data updated with new entries."})
    else:
        return jsonify({"success": False, "message": "No new data to update."})


@app.route('/data')
def data():
    conn = create_connection()

    # Assuming we have 4 fields to retrieve and plot
    field_numbers = [1, 2, 3, 4]
    n_points = 36  # The number of points to retrieve

    # Prepare the data for all fields
    data_for_frontend = {}
    for field_number in field_numbers:
        field_data = get_data_for_plotting(conn, field_number, n_points)
        # Store the data using the field number as a key
        data_for_frontend[f'field{field_number}'] = field_data

    print(f"Data for frontend: {data_for_frontend}")

    # Close the database connection
    conn.close()

    # Return the data as JSON
    return jsonify(data_for_frontend)

@app.route('/favicon.ico')
def favicon():
    # Serve the favicon - ensure there is a favicon.ico file in the static directory.
    return send_from_directory(app.static_folder, 'static/favicon.ico')


# Add routes for apple touch icons if needed
@app.route('/apple-touch-icon.png')
@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon():
    # Serve the apple touch icon - ensure there is an apple-touch-icon.png file in the static directory.
    return send_from_directory(app.static_folder, 'apple-touch-icon.png')

# Make sure to have a 404 error handler to customize
