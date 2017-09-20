from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from .models import ShoppingList

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    
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
    return app