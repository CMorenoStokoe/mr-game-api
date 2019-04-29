import os, os.path

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.edges import EdgeList, Edges, Edge
from resources.annot import AnnotList, Annots, Home, AnnotDel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'authKey01'
api = Api(app)
CORS(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Home, '/')
api.add_resource(EdgeList, '/edges')
api.add_resource(Edges, '/edges/<string:exp_name>')
api.add_resource(Edge, '/edges/<string:exp_name>/<string:out_name>')
api.add_resource(AnnotList, '/annotations')
api.add_resource(Annots, '/annotations/<string:exp_name>/<string:out_name>')
api.add_resource(UserRegister, '/register')
api.add_resource(AnnotDel, '/annotations/del/<string:exp_name>/<string:out_name>/<string:username>')

if os.path.isfile("data.db"):
	print("Message: data.db already exists.")
else:
	from create_tables import *

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)
	