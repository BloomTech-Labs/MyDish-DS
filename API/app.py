import os
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from decouple import config
import logging


# setting up for local testing, wnat to be able to log the database
"""
Want to be able to test locally and log information for debugging 
"""

# Local sqlite3 database
local_db = 'test.sqlite3'


def create_app(test_config=None):
    """
    Creates app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Make sure to change debug to False in production env
        DEBUG=config('DEBUG', default=False),
        SECRET_KEY=config('SECRET_KEY', default='dev'),  # CHANGE THIS!!!!
        # For in-memory db: default='sqlite:///:memory:'),
        DATABASE_URI=config('DATABASE_URI', 'sqlite:///' + \
                            os.path.join(os.getcwd(), local_db_name)),
        LOGFILE=config('LOGFILE', os.path.join(
            app.instance_path, 'logs/debug.log')),
        CACHE_TYPE=config('CACHE_TYPE', 'simple'),  # Configure caching
        # Long cache times probably ok for ML api
        CACHE_DEFAULT_TIMEOUT=config('CACHE_DEFAULT_TIMEOUT', 300),
        TESTING=config('TESTING', default='TRUE')
    )

    # Enable CORS header support
    CORS(app)

    # Enable caching
    cache = Cache(app)
