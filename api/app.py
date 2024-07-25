from flask import Flask 
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'beer_db'
db = MySQL(app)

# Import routes
from routes.auth import register, logout, login
from routes.beer import newBeer, allBeers, searchBeers
from routes.events import newEvents, allEvents
from routes.event_participants import newEventParticipant, allEventParticipant
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



if __name__ == '__main__':
    app.run(debug=True)