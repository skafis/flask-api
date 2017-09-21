from flask import Flask, request, jsonify, abort, session, make_response
from flask_httpauth import HTTPBasicAuth
from flask_api import FlaskAPI
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

auth = HTTPBasicAuth()
db = SQLAlchemy()

def create_app(config_name):
    from .models import ShoppingList, Users

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/users/<int:id>')
    def get_user(id):
        user = Users.query.get(id)
        if not user:
            app.logger.error("No user Found")
            return jsonify({'result': status})

        return jsonify({'username': user.username})

    @app.route('/api/token')
    @auth.login_required
    def get_auth_token():
        token = g.user.generate_auth_token()
        return jsonify({ 'token': token.decode('ascii') })


    @auth.verify_password
    def verify_password(username_or_token, password):

        # first try to authenticate by token
        user = Users.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = Users.query.filter_by(username=username_or_token).first()

            if not user or not user.verify_password(password):

                return False
        g.user = user
        return True

    @app.route('/api/dashboard/', methods=['POST','GET'])
    def shoppinglists():

        # Get the access token from the header
        auth_header = str(request.headers.get('Authorization'))
        print(auth_header)
        access_token = auth_header.split(" ")

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = Users.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":

                    title = str(request.data.get('title', ''))

                    if title:

                         shoplist =ShoppingList(title=title, created_by=user_id)
                         shoplist.save()
                         response= jsonify({
                             'id': shoplist.id,
                             'title': shoplist.title,
                             'created_by': user_id
                         })
                         
                         return make_response(response), 201
                else:
                    # all shopping list
                    shoplist = ShoppingList.get_all()
                    results = []

                    for shop_list in shoplist:
                        obj = {
                            'id': shop_list.id,
                            'title': shop_list.title
                        }
                        results.append(obj)
                    
                    return make_response(jsonify(results)), 200

            else:

                # user not verified
                message = user_id
                response = {
                    'message' : message
                }
                return make_response(jsonify(response)), 401


    @app.route('/api/dashboard/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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


      # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app