import firebase_admin

from flask import Flask
from flask_restful import Api
from firebase_admin import db
from firebase_admin import credentials

app = Flask(__name__)
api = Api(app)

"""
Initialize the app with a service account, 
granting admin privileges
"""
firebase_admin.initialize_app(
    credentials.Certificate("firebase.service.json"),
    {'databaseURL': 'https://kopinema-cc4c2.firebaseio.com/'}
)

"""
As an admin, 
the app has access to read and write all data, 
regradless of Security Rules
"""
ref = db.reference('database')

from resource import Board, Queue, Served

api.add_resource(Board, '/board')
api.add_resource(Queue, '/queue/<id>')
api.add_resource(Served, '/served')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
