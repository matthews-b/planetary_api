from flask_marshmallow import Marshmallow
from flask import Flask

app = Flask(__name__)
ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
