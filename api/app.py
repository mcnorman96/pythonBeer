import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()  # load variables from .env
import pymysql
pymysql.install_as_MySQLdb()

# Initialize Flask app
app = Flask(__name__)

# Configure database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:"
    f"{os.getenv('MYSQL_PASSWORD', '')}@"
    f"{os.getenv('MYSQL_HOST', 'localhost')}/"
    f"{os.getenv('MYSQL_DB', 'beer_db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

from models import *

# Import routes
from routes.auth import register, logout, login
from routes.beer import newBeer, allBeers, searchBeers
from routes.events import newEvents, allEvents
from routes.event_participant import newEventParticipant, allEventParticipant
from routes.event_beer import newEventBeer, allEventBeer
from routes.ratings import newRatings, allRatings, toplistRatings, toplistRatingsByEvent

# Register blueprints
app.register_blueprint(register, url_prefix='/auth/')
app.register_blueprint(login, url_prefix='/auth/')
app.register_blueprint(logout, url_prefix='/auth/')

app.register_blueprint(newBeer, url_prefix='/beer/')
app.register_blueprint(allBeers, url_prefix='/beer/')
app.register_blueprint(searchBeers, url_prefix='/beer/')

app.register_blueprint(newEvents, url_prefix='/events/')
app.register_blueprint(allEvents, url_prefix='/events/')
app.register_blueprint(newEventParticipant, url_prefix='/events/')
app.register_blueprint(allEventParticipant, url_prefix='/events/')
app.register_blueprint(newEventBeer, url_prefix='/events/')
app.register_blueprint(allEventBeer, url_prefix='/events/')

app.register_blueprint(newRatings, url_prefix='/ratings/')
app.register_blueprint(allRatings, url_prefix='/ratings/')
app.register_blueprint(toplistRatings, url_prefix='/ratings/')
app.register_blueprint(toplistRatingsByEvent, url_prefix='/ratings/')

@app.route('/')
def index():
    return "Beer event rating API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
