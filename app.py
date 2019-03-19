import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.edges import EdgeList, Edge
from resources.annot import AnnotList, Annot, Home

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'authKey01'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Home, '/')
api.add_resource(EdgeList, '/edges')
api.add_resource(Edge, '/edges/<int:ref>')
api.add_resource(AnnotList, '/annotations')
api.add_resource(Annot, '/annotations/<int:ref>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)
	