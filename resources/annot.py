import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.annot import AnnotModel
from models.edges import EdgeModel

class Home(Resource):
	def get(self):
		return "Hello, World!"


class AnnotList(Resource):
	def get(self):
		return {'annotations': [annotation.json() for annotation in AnnotModel.query.all()]}


class Annots(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
	type=str,
	)
	parser.add_argument('judgement',
	type=int,
	)
	parser.add_argument('comment',
	type=str,
	)
	
	def get(self, exp_name):
		edge = AnnotModel.find_annots_by_expName(exp_name)
		if edge:
			return edge
		return {'message': "{} not found in db".format(exp_name)}, 404

	#@jwt_required() - disabled for testing
	#need to add proper post/put method
	def post(self, exp_name):
		data = Annot.parser.parse_args()

		ref = EdgeModel.expName_to_ref(exp_name)
		username = data['username']

		annotExists = AnnotModel.find_annots_by_refAndUsr(ref, username) 
		if annotExists:
			return {"Message": "Annotation already made by user {}, please use PUT to update instead".format(username), 'Existing annotation': annotExists}
		newAnnot = AnnotModel(
								None, 
								ref, 
								data['username'], 
								data['judgement'], 
								data['comment']
						)
		newAnnot.save_to_db()
		return {'Message': "Annotation made successfully", 'Preview': newAnnot.json()}, 404

	def put(self, exp_name):
		data = Annot.parser.parse_args()

		ref = EdgeModel.expName_to_ref(exp_name)
		username = data['username']

		return AnnotModel.update_annots_by_ref(ref, username)

	def delete(self, exp_name):
		edge = AnnotModel.find_annots_by_expName(exp_name)
		if edge:
			annot.delete_from_db()
			return {'message' : "Annotation deleted"}
		return {'message': "{} not found in db".format(exp_name)}, 404

class Annot(Resource):
	def get(self,exp_name,out_name, infoReq):
		infoReq = Annotations
		edge = EdgeModel.find_edge_by_expNameAndOutName(exp_name,out_name,infoReq)
		if edge:
			return edge
		return {'message': '{} not found in db'.format(exp_name)}, 404