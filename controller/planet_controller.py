from model.planet_model import Planet
from flask import jsonify

class PlanetController:

    @staticmethod
    def db_seed():
        return Planet.db_seed()

    @staticmethod
    def get_all_planets():
        return Planet.get_all_planets()

    @staticmethod
    def planet_details(planet_id):
        return Planet.planet_details(planet_id)

    @staticmethod
    def add_planet(planet_name, planet_type, home_star, mass, radius, distance):
        planet_name = planet_name
        test = Planet.find_by_planet_name(planet_name=planet_name)
        if test:
            return jsonify(message='Planet name already exists'), 409
        else:
            Planet.add_planet(planet_name, planet_type, home_star, mass, radius, distance)
            return jsonify(message="New planet added"), 201

    @staticmethod
    def update_planet(planet_id, planet_name, planet_type, home_star, mass, radius, distance):
        planet = Planet.find_by_planet_id(planet_id=planet_id)
        if planet:
            Planet.update_planet(planet_id, planet_name, planet_type, home_star, mass, radius, distance)
        return jsonify(message="Planet successfully updated"), 201

    @staticmethod
    def remove_planet(planet_id):
        return Planet.remove_planet(planet_id)

