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

    user1 = User(username="alice", password=generate_password_hash("password1"), email="alice@example.com")
    user2 = User(username="bob", password=generate_password_hash("password2"), email="bob@example.com")
    db.session.add_all([user1, user2])
    db.session.commit()

    event1 = Event(
        name="Summer Beer Fest",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=1),
        description="A fun event to taste summer beers!"
    )
    db.session.add(event1)
    db.session.commit()

    participant1 = EventParticipant(event_id=event1.id, user_id=user1.id, joined_at=datetime.utcnow())
    participant2 = EventParticipant(event_id=event1.id, user_id=user2.id, joined_at=datetime.utcnow())
    db.session.add_all([participant1, participant2])
    db.session.commit()

    beer1 = Beer(name="Golden Ale", description="Light and crisp", brewery="Brewery A", type="Ale")
    beer2 = Beer(name="Dark Stout", description="Rich and creamy", brewery="Brewery B", type="Stout")
    db.session.add_all([beer1, beer2])
    db.session.commit()

    event_beer1 = EventBeer(event_id=event1.id, beer_id=beer1.id, added_at=datetime.utcnow())
    event_beer2 = EventBeer(event_id=event1.id, beer_id=beer2.id, added_at=datetime.utcnow())
    db.session.add_all([event_beer1, event_beer2])
    db.session.commit()

    rating1 = Rating(event_id=event1.id, beer_id=beer1.id, user_id=user1.id, taste=8, aftertaste=7, smell=8, design=5, score=7, rated_at=datetime.utcnow())
    rating2 = Rating(event_id=event1.id, beer_id=beer2.id, user_id=user2.id, taste=9, aftertaste=8, smell=7, design=6, score=8, rated_at=datetime.utcnow())
    db.session.add_all([rating1, rating2])
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():  # <--- This is critical!
        seed()
