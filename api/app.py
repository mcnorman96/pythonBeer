import os
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv


load_dotenv()
import pymysql

pymysql.install_as_MySQLdb()
from db import db, migrate
from socketio_instance import socketio


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
socketio.init_app(app, cors_allowed_origins="*")

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

## Docs
SWAGGER_URL = '/api/docs'
API_URL = '/api/openapi.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PythonBeer API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/api/openapi.yaml')
def send_openapi():
    return send_from_directory('./', 'openapi.yaml')

@app.route("/")
def index():
    return "Beer event rating API is running!"



if __name__ == "__main__":
    import sys
    debug_mode = False
    if "--reload" in sys.argv:
        debug_mode = True
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
