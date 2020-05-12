'''
Entry point for the app
'''

from app.application import create_app

APP = create_app()
APP.run(debug=True)
