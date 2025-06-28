from db import db
class Beer(db.Model):
    __tablename__ = 'beer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    brewery = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'brewery': self.brewery,
            'type': self.type
        }
