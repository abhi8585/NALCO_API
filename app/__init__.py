# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, url_for,current_app
from importlib import import_module
from os import path
from logging import basicConfig, DEBUG, getLogger, StreamHandler
# db = SQLAlchemy()
# login_manager = LoginManager()
# mail=Mail()



# def register_extensions(app):
#     db.init_app(app)
#     login_manager.init_app(app)
#     mail.init_app(app)

def register_blueprints(app):
    for module_name in ('master','delivery','modify','loadplanning'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

# def configure_database(app):

#     @app.before_first_request
#     def initialize_database():
#         db.create_all()

#     @app.teardown_request
#     def shutdown_session(exception=None):
#         db.session.remove()



def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    # register_extensions(app)
    register_blueprints(app)
    # configure_database(app)
    with app.app_context():
       CONFIG=current_app.config
    return app

