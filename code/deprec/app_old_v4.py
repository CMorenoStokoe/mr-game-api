from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from edges import Status, View, Edge, Annotate, Annotation

app = Flask(__name__)
app.secret_key = 'authKey01' #auth disabled for testing in current build
api = Api(app)

api.add_resource(Status, '/status')
api.add_resource(View, '/view/<string:database>')
api.add_resource(Edge, '/edge/<string:ref>')
api.add_resource(Annotation, '/annotation/<string:annotID>')
api.add_resource(Annotate, '/annotate')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	app.run(port=5000, debug=True)