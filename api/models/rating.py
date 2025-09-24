from db import db

class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    beer_id = db.Column(db.Integer, db.ForeignKey('beer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    taste = db.Column(db.Float, nullable=False)
    aftertaste = db.Column(db.Float, nullable=False)
    smell = db.Column(db.Float, nullable=False)
    design = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'beer_id': self.beer_id,
            'user_id': self.user_id,
            'taste': self.taste,
            'aftertaste': self.aftertaste,
            'smell': self.smell,
            'design': self.design,
            'score': self.score
        }