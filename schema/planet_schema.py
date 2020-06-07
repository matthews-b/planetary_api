from flask_marshmallow import Marshmallow
from flask import Flask

app = Flask(__name__)
ma = Marshmallow(app)


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')
