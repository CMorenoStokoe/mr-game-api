import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.edges import EdgeList, Edge
from resources.annot import AnnotList, Annot, Home

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgres://kcabvtljvflpnc:a1e491d35733f7784b7fc3e3c205a3794b45c3e383abacd398ea0928e326112e@ec2-79-125-4-72.eu-west-1.compute.amazonaws.com:5432/d5r274ufjsq4v9','sqlite:///data.db')
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
	