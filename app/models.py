from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import db

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

    @auth.verify_password
    def verify_password(username_or_token, password):
        # first try to authenticate by token
        user = Users.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = Users.query.filter_by(username = username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        return True

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