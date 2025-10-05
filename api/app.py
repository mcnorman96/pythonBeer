import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
import pymysql

pymysql.install_as_MySQLdb()
from db import db, migrate
from flask_socketio import SocketIO


logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "DEBUG"),
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "")

# Configure database URI from environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:"
    f"{os.getenv('MYSQL_PASSWORD', '')}@"
    f"{os.getenv('MYSQL_HOST', 'localhost')}/"
    f"{os.getenv('MYSQL_DB', 'beer_db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and migration objects
db.init_app(app)
migrate.init_app(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Import routes
from routes.auth import auth_bp
from routes.beer import beer_bp
from routes.event import event_bp
from routes.event_participant import event_participant_bp
from routes.event_beer import event_beer_bp
from routes.ratings import ratings_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth/")
app.register_blueprint(beer_bp, url_prefix="/beer/")
app.register_blueprint(event_bp, url_prefix="/events/")
app.register_blueprint(event_participant_bp, url_prefix="/events/")
app.register_blueprint(event_beer_bp, url_prefix="/events/")
app.register_blueprint(ratings_bp, url_prefix="/ratings/")


@app.route("/")
def index():
    return "Beer event rating API is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
