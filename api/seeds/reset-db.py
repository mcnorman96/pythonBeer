from datetime import datetime, timedelta
from app import app, db  # Make sure `app` is your Flask app instance
from models.user import User
from models.event import Event
from models.beer import Beer
from models.event_participant import EventParticipant
from models.event_beer import EventBeer
from models.rating import Rating
from werkzeug.security import generate_password_hash


def seed():
    # Optional: Clear old data
    # db.session.query(...).delete()
    db.drop_all()
    db.create_all()

    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():  # <--- This is critical!
        seed()
