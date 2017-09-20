from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config


db = SQLAlchemy()

def create_app(config_name):
    from .models import ShoppingList, Users

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/auth/register/', methods = ['POST'])
    def new_user():
        # json_data = request.json
        username =str(request.data.get('username', '')),
        email=str(request.data.get('email', '')),
        password=str(request.data.get('password', ''))

        if username is None or password is None:
            abort(400) # missing arguments

        if Users.query.filter_by(username = username).first() is not None:
            abort(400) # existing user

        user = Users(username = username)
        # user.hash_password(password)

        # save user session to db
        db.session.add(user)
        db.session.commit()

        return jsonify({ 'username': user.username }), 201,
        {'Location': url_for('get_user', id = user.id, _external = True)}

    @app.route('/shopinglists/', methods=['POST','GET'])
    def shoppinglists():
        if request.method == "POST":
            title = str(request.data.get('title', ''))
            if title:
                 shoplist =ShoppingList(title=title)
                 shoplist.save()
                 response= jsonify({
                     'id': shoplist.id,
                     'title': shoplist.title
                 })
                 response.status_code = 201
                 return response
        else:
            shoplist = ShoppingList.get_all()
            results = []

            for shop_list in shoplist:
                obj = {
                    'id': shop_list.id,
                    'title': shop_list.title
                }
                results.append(obj)
            response= jsonify(results)
            response.status_code= 200
            return response


    @app.route('/shopinglists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def get_shopping_list(id, **kwargs):
     # retrieve list ids 
        shoplist = ShoppingList.query.filter_by(id=id).first()
        if not shoplist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            shoplist.delete()
            return {
            "message": "The Shoping list {} deleted successfully".format(shoplist.id) 
         }, 200

        elif request.method == 'PUT':
            title = str(request.data.get('title', ''))
            shoplist.title = title
            shoplist.save()
            response = jsonify({
                'id': shoplist.id,
                'title': shoplist.title,
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': shoplist.id,
                'title': shoplist.title
            })
            response.status_code = 200
            return response
    return app