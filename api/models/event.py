from app import db

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'description': self.description,
        }