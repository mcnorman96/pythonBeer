from app import db
from models.event import Event

class EventBeer(db.Model):
    __tablename__ = 'event_beer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    beer_id = db.Column(db.Integer, db.ForeignKey('beer.id'), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'beer_id': self.beer_id,
            'added_at': self.added_at,
        }