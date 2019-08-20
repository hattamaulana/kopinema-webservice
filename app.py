import firebase_admin

from flask import Flask
from flask_restful import Api
from firebase_admin import db
from firebase_admin import credentials


app = Flask(__name__)
api = Api(app)
cred = credentials.Certificate("firebase.service.json")

"""
Initialize the app with a service account, 
granting admin privileges
"""
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kopinema-cc4c2.firebaseio.com/'
})

"""
As an admin, 
the app has access to read and write all data, 
regradless of Security Rules
"""
ref = db.reference('database')

"""
Register API
"""
import API

api.add_resource(API.Board, '/board')
api.add_resource(API.Queue, '/queue/<id>')
api.add_resource(API.Served, '/served')

if __name__ == '__main__':
    app.run(host='192.168.1.4', debug=False)
