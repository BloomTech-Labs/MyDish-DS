from flask import Flask
import os
from os import getenv
import psycopg2
from app.route.routes import all_routes


"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
there is a need to implement exception handling when the picture that was
taken is that unclear that the google vision api does not return any text
in texts[0].description
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


def create_app():
    '''
    Application factory
    '''
    app = Flask(__name__)

    # Registering routes
    app.register_blueprint(all_routes)

    return app
