from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask import jsonify
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    @staticmethod
    def register(email, first_name, last_name, password):
        test = User.query.filter_by(email=email).first()
        if test:
            return jsonify(message='That email already exists.'), 409
        else:
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify(message='User created successfully.'), 201

    @staticmethod
    def find_by_email_and_password(email, password):
        return User.query.filter_by(email=email, password=password).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
