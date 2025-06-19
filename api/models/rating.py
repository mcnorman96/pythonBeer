from app import db

class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    beer_id = db.Column(db.Integer, db.ForeignKey('beer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    taste = db.Column(db.Integer, nullable=False)
    aftertaste = db.Column(db.Integer, nullable=False)
    smell = db.Column(db.Integer, nullable=False)
    design = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    rated_at = db.Column(db.DateTime, nullable=False)
