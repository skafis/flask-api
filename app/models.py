import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask import current_app

# from passlib.apps import custom_app_context as pwd_context
from flask_api import FlaskAPI
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from instance.config import app_config
from app import db

app = FlaskAPI(__name__, instance_relative_config=True)
class Users(db.Model):
    """
    users table
    """
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300))
    email = db.Column(db.String(300))
    password = db.Column(db.String(128))

    def __init__(self, email, password):
        '''
        initialize class
        '''
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()


    def save(self):
        """
        Save a user to the database.
        """
        db.session.add(self)
        db.session.commit()


    def verify_password(self, password):
        '''
        check pasword provided with hash in db
        '''
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)


    @staticmethod
    def is_active(self):
        # make all user active
        return True

    @staticmethod
    def get_all(user_id):
        """This method gets all the bucketlists for a given user."""
        return ShoppingList.query.filter_by(created_by=user_id)

    
    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def delete(self):
        """Deletes a given shoppings."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of a lists instance."""
        return "<ShoppingList: {}>".format(self.name)



class ShoppingList(db.Model):
    """
    shopping list table
    """
    __tablename__ = 'shoppinglists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        """initialize with title."""
        self.title = title

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ShoppingList.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<ShoppingList: {}>".format(self.title)