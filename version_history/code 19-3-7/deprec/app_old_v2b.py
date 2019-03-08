from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'authKey01'
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
		'annotation':'smoking is good for you'
	}
]

	#get status (debug)
class Status(Resource):
	def get(self):
		return {'Status' : '200 OK'}

	#get list of edges
class View(Resource):
	def get(self, database):
		if database == "edges":
			return edges
		elif database == "annotations":
			return annotations
		else:
			return "Database {} not found".format(database), 404

	#request parser is slated for removal, use marshmallow instead
class Edge(Resource):
	parser = reqparse.RequestParser()
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
		return {'edge': edge}, 200 if edge else 404

	#post new edge
	def post(self,ref):
		if next(filter(lambda x: x['ref']==ref,edges), None):
			return {'message':"A ref with name '{}' already exists.".format(ref)}, 400

		data = Edge.parser.parse_args()
		edge = {
					'ref': ref,
					'exposure': data['exposure'],
					'outcome': data['outcome'], 
					'annotations': data['annotations']
				}
		edges.append(edge)
		return edge, 201

	#delete edge by ref
	def delete(self, ref):
		global edges
		edges = list(filter(lambda x: x['ref'] !=ref, edges))
		return {'message':'item deleted'}

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
		edge = next(filter(lambda x: x['ref']==ref,edges), None)
		#next selects one item, list selects multiple items
		return edge['annotations']
		#{'edge': edge}, 200 if edge else 404

	#put (update/create) new annotation
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
			return edge, 201
		else:
			return {'message':"A ref with name '{}' does not exist.".format(ref)}, 400

	#delete annotation by ref
	def delete(self, ref):
		global edges
		edges = list(filter(lambda x: x['ref'] !=ref, edges))
		return {'message':'item deleted'}


	

api.add_resource(Status, '/status')
api.add_resource(View, '/view/<string:database>')
api.add_resource(Edge, '/edge/<string:ref>')
api.add_resource(Annotate, '/annotate/<string:ref>')

app.run(port=5000)