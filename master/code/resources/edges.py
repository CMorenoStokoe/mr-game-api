import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.edges import EdgeModel

class EdgeList(Resource):
	def get(self):
		return {'edges': [edge.json() for edge in EdgeModel.query.all()]}


class Edge(Resource):
	def get(self,ref):
		edge = EdgeModel.find_edges_by_ref(ref)
		if edge:
			return edge.json()
		return {'message': '{} not found in db'.format(ref)}, 404

