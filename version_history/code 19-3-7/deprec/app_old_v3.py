from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import User, UserRegister

app = Flask(__name__)
app.secret_key = 'authKey01' #auth disabled for testing in current build
api = Api(app)

jwt = JWT(app, authenticate, identity)

edges=[
	{
		'ref': '22479202-23128233', # unique identifiers for each edge
		'exposure':22479202, #PubmedID
		'exp_name':"Adiponectin",
		'outcome':23128233, #PubmedID
		'out_name':"Crohn's disease"
	}
]

annotations=[
	{
		'ref': '22479202-23128233',
		'username':'chris',
		'judgement':0, # binary ; whether they think the edge is real or not
		'annotation':'These cannot be related'
	}
]

	#get status (debug)
class Status(Resource):
	def get(self):
		return 'OK', 200

	#get list of edges
class View(Resource):
	def get(self, database):
		if database == "edges":
			return edges
		elif database == "annotations":
			return annotations
		else:
			return {'message':'Database {} not found'.format(database)}, 404

class Edge(Resource):
	parser = reqparse.RequestParser() #request parser slated for removal, move to marshmallow 
	parser.add_argument('ref',
		type=str,
	)
	parser.add_argument('exposure',
		type=int,
	)
	parser.add_argument('exp_name',
		type=str,
	)
	parser.add_argument('outcome',
		type=int,
	)
	parser.add_argument('out_name',
		type=str,
	)

	#get edge by ref
	def get(self,ref):
		edge = next(filter(lambda x: x['ref']==ref,edges), None)
		#next selects one item, list selects multiple items
		if edge != None:
			return {'edge': edge}, 200
		else:
			return {'message':'No edge with ref {} found.'.format(ref)}, 404

class Annotate(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('ref',
		type=str,
	)
	parser.add_argument('username',
		type=str,
	)
	parser.add_argument('judgement',
		type=int,
	)
	parser.add_argument('annotation',
		type=str,
	)

	#get annotations by ref
	def get(self,ref):
		annotation = next(filter(lambda x: x['ref']==ref,annotations), None)
		if annotation != None:
			return annotation, 200
		else:
			return {'message':'No annotations for {} found.'.format(ref)}, 404

	#put (update/create) new annotation
	@jwt_required()
	def put(self,ref):
		edge = next(filter(lambda x: x['ref']==ref,edges), None)
		if edge != None:

			data = Annotate.parser.parse_args()
			annotations.append(
				{
					'ref':data['ref'],
					'username':data['username'],
					'judgement':data['judgement'],
					'annotation':data['annotation']
				}
			)
			return {'message':'Annotation added'}, 201
		else:
			return {'message':'An edge with ref {} was not found.'.format(ref)}, 400

	#delete annotation by ref
	@jwt_required()
	def delete(self, ref):
		global edges
		edges = list(filter(lambda x: x['ref'] !=ref, edges))
		return {'message':'item deleted'}

api.add_resource(Status, '/status')
api.add_resource(View, '/view/<string:database>')
api.add_resource(Edge, '/edge/<string:ref>')
api.add_resource(Annotate, '/annotate/<string:ref>')
api.add_resource(UserRegister, '/register')

app.run(port=5000)