from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.edges import Status, View, Edge, Annotate, Annotation

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'authKey01'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Status, '/status')
api.add_resource(View, '/view/<string:database>')
api.add_resource(Edge, '/edge/<string:ref>')
api.add_resource(Annotation, '/annotation/<string:ref>')
api.add_resource(Annotate, '/annotate')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)