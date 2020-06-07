import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required


from controller.planet_controller import PlanetController
from controller.user_controller import UserController

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'ee36770550cf58'
app.config['MAIL_PASSWORD'] = '986dcd6194c738'

jwt = JWTManager(app)
db = SQLAlchemy(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


@app.cli.command('db_seed')
def db_seed():
    PlanetController.db_seed()
    print('Database seeded!')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API')


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource is not found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough.")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name, age):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough.")


@app.route('/planets', methods=['GET'])
def planets():
    return PlanetController.get_all_planets()


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    return UserController.register(email, first_name, last_name, password)


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    return UserController.login(email, password)


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email):
    # won't work
    return UserController.retrieve_password(email)


@app.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id):
    return PlanetController.planet_details(int(planet_id))


@app.route('/add_planet', methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.form['planet_name']
    planet_type = request.form['planet_type']
    home_star = request.form['home_star']
    mass = float(request.form['mass'])
    radius = float(request.form['radius'])
    distance = float(request.form['distance'])
    return PlanetController.add_planet(planet_name, planet_type, home_star, mass, radius, distance)


@app.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    planet_id = request.form['planet_id']
    planet_name = request.form['planet_name']
    planet_type = request.form['planet_type']
    home_star = request.form['home_star']
    mass = float(request.form['mass'])
    radius = float(request.form['radius'])
    distance = float(request.form['distance'])
    return PlanetController.update_planet(planet_id, planet_name, planet_type, home_star, mass, radius, distance)


@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required
def remove_planet(planet_id):
    return PlanetController.remove_planet(planet_id)


if __name__ == '__main__':
    app.run(debug=True)
