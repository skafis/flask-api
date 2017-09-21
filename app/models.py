from passlib.apps import custom_app_context as pwd_context
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
    password_hash = db.Column(db.String(128))

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password
    #     self.authenticated = False

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def is_active(self):
        # make all user active
        return True

    def get_id(self):
        # return email adress for flask login
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        # Dont support anonymus users
        return False

    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = Users.query.get(data['id'])
        return user



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