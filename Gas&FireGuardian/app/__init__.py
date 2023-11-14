from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

# Import routes after app and scheduler initialization to avoid circular imports
from app import routes

# Initialize the scheduler
scheduler.init_app(app)
scheduler.start()
