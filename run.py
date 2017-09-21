import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from app import create_app

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

if __name__ == '__main__':
	handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
    app.run()