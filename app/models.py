from app import db

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