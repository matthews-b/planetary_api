from flask_sqlalchemy import SQLAlchemy
from schema.planet_schema import PlanetSchema
from sqlalchemy import Column, Integer, String, Float
from flask import jsonify
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

    @staticmethod
    def db_seed():
        mecury = Planet(planet_name='Mecury',
                        planet_type='Class D',
                        home_star='Sol',
                        mass=3.258e23,
                        radius=1516,
                        distance=35.98e6)

        venus = Planet(planet_name='Venus',
                       planet_type='Class K',
                       home_star='Sol',
                       mass=4.867e24,
                       radius=3760,
                       distance=67.24e6)

        earth = Planet(planet_name='Earth',
                       planet_type='Class M',
                       home_star='Sol',
                       mass=5.972e24,
                       radius=3959,
                       distance=92.96e6)

        db.session.add(mecury)
        db.session.add(venus)
        db.session.add(earth)

        test_user = User(first_name='Mark',
                         last_name='Monroe',
                         email='test@test.com',
                         password='P@ssw0rd')

        db.session.add(test_user)
        db.session.commit()
        return

    @staticmethod
    def find_by_planet_id(planet_id):
        return Planet.query.filter_by(planet_id=planet_id).first()

    @staticmethod
    def find_by_planet_name(planet_name):
        return Planet.query.filter_by(planet_name=planet_name).first()

    @staticmethod
    def get_all_planets():
        planets_list = Planet.query.all()
        result = planets_schema.dump(planets_list)
        return jsonify(result)

    @staticmethod
    def planet_details(planet_id):
        planet = Planet.find_by_planet_id(planet_id)
        if planet:
            result = planet_schema.dump(planet)
            return jsonify(result)
        else:
            return jsonify(message='Planet does not exist'), 404

    @staticmethod
    def add_planet(planet_name, planet_type, home_star, mass, radius, distance):

        new_planet = Planet(planet_name=planet_name,
                            planet_type=planet_type,
                            home_star=home_star,
                            mass=mass,
                            radius=radius,
                            distance=distance)

        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="New planet added"), 201

    @staticmethod
    def update_planet(planet_id, planet_name, planet_type, home_star, mass, radius, distance):
        planet = Planet.query.filter_by(planet_id=planet_id).first()
        if planet:
            planet.planet_name = planet_name
            planet.planet_type = planet_type
            planet.home_star = home_star
            planet.mass = mass
            planet.radius = radius
            planet.distance = distance
            db.session.commit()
            return jsonify(message='Planet successfully updated'), 202
        else:
            return jsonify(message='Planet does not exist'), 404

    @staticmethod
    def remove_planet(planet_id):
        planet = Planet.find_by_planet_id(planet_id=planet_id)
        if planet:
            db.session.delete(planet)
            db.session.commit()
            return jsonify(message='Planet successfully deleted'), 202
        else:
            return jsonify(message='Planet does not exist'), 404

