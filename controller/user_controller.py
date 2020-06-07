from model.user_model import User
from flask_mail import Mail, Message
from flask_jwt_extended import create_access_token
from flask import jsonify
from flask import Flask

app = Flask(__name__)
mail = Mail(app)


class UserController:

    @staticmethod
    def register(email, first_name, last_name, password):
        return User.register(email, first_name, last_name, password)

    @staticmethod
    def login(email, password):
        test = User.find_by_email_and_password(email=email, password=password)
        if test:
            access_token = create_access_token(identity=email)
            return jsonify(message='Login successful!', access_token=access_token)
        else:
            return jsonify(message='Incorrect email or password'), 401

    @staticmethod
    def retrieve_password(email):
        user = User.find_by_email(email=email)
        if user:
            msg = Message('Your planetary password is ' + user.password,
                          sender="admin@planetery-api.com",
                          recipients=[email])
            mail.send(msg)
            return jsonify(message='Password sent to ' + email)
        else:
            return jsonify(message='email does not exit'), 401
