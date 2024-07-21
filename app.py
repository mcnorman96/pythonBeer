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
# Register blueprints
app.register_blueprint(register, url_prefix='/auth/')
app.register_blueprint(login, url_prefix='/auth/')
app.register_blueprint(logout, url_prefix='/auth/')
app.register_blueprint(newBeer, url_prefix='/beer/')
app.register_blueprint(allBeers, url_prefix='/beer/')
app.register_blueprint(searchBeers, url_prefix='/beer/')


if __name__ == '__main__':
    app.run(debug=True)