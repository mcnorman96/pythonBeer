import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()
import pymysql
pymysql.install_as_MySQLdb()
from db import db, migrate
from flask_socketio import SocketIO, emit

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "DEBUG"),
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '')

# Configure database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:"
    f"{os.getenv('MYSQL_PASSWORD', '')}@"
    f"{os.getenv('MYSQL_HOST', 'localhost')}/"
    f"{os.getenv('MYSQL_DB', 'beer_db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration objects
db.init_app(app)
migrate.init_app(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Import routes
from routes.auth import register, logout, login
from routes.beer import newBeer, allBeers, searchBeers
from routes.event import newEvents, allEvents
from routes.event_participant import newEventParticipant, allEventParticipant
from routes.event_beer import newEventBeer
from routes.ratings import newRatings, getRating, getAllRatingsForBeer, toplistRatings, toplistRatingsByEvent

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

app.register_blueprint(newRatings, url_prefix='/ratings/')
app.register_blueprint(getRating, url_prefix='/ratings/')
app.register_blueprint(getAllRatingsForBeer, url_prefix='/ratings/')
app.register_blueprint(toplistRatings, url_prefix='/ratings/')
app.register_blueprint(toplistRatingsByEvent, url_prefix='/ratings/')

@app.route('/')
def index():
    return "Beer event rating API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
