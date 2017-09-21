from flask import Flask, request, jsonify, abort, session
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

    @app.route('/auth/register/', methods = ['POST'])
    def new_user():
        # json_data = request.json
        username =str(request.data.get('username', '')),
        email=str(request.data.get('email', '')),
        password=str(request.data.get('password', ''))

        app.logger.warning('A warning occurred (%d apples)', 42)
        app.logger.error('An error occurred')
        app.logger.info('Info')
        
        if username is None or password is None:
            status = 'input can not be empty '# missing arguments
            return jsonify({'result': status})

        if Users.query.filter_by(username = username).first() is not None:
            status = 'this user is already registered'# existing user

        user = Users(username = username)
        user.hash_password(password)

        # save user session to db
        db.session.add(user)
        db.session.commit()

        return jsonify({ 'username': user.username}), 201,
        {'Location': url_for('get_user', id = user.id, _external = True)}

    # return the user

    @app.route('/api/users/<int:id>')
    def get_user(id):
        user = Users.query.get(id)
        if not user:
            status = "No user Found"
            return jsonify({'result': status})

        return jsonify({'username': user.username})

    # login  method 
    @app.route('/auth/login', methods=['POST'])
    def login():
        password=str(request.data.get('password', ''))
        user = User.query.filter_by(username =str(request.data.get('username', ''))).first()

        if user and user.hash_password(password):
            session['logged_in'] = True
            status = True

        else:
            status = False

        return jsonify({'result': status})

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