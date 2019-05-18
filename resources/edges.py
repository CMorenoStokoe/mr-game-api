import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.edges import EdgeModel

class EdgeList(Resource):
	def get(self):
		return {'edges': [edge.json() for edge in EdgeModel.query.all()]}


class Edges(Resource):
	def get(self,exp_name):
		edges = EdgeModel.find_edges_by_expName(exp_name)
		if edges:
			return {"edges" : edges}
		return {'message': '{} not found in db'.format(exp_name)}, 404

class Edge(Resource):
	def get(self,exp_name,out_name):
		edge = EdgeModel.find_edge_by_expNameAndOutName(exp_name,out_name)
		if edge:
			return edge
		return {'message': '{} not found in db'.format(exp_name)}, 404