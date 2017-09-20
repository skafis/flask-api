from passlib.apps import custom_app_context as pwd_context

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

    @staticmethod
    def hash_password(self):
        self.password_hash = pwd_context.encrypt()

    def is_active(self):
        # make all user active
        return True

    def get_id(self):
        # return email adress for flask login
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def check_password(self, hashed_password, password):
        # return true or false
        pwd_context.verify(password, self.password)

    def is_anonymous(self):
        # Dont support anonymus users
        return False

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