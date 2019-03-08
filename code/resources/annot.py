import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.annot import AnnotModel

class AnnotList(Resource):
	def get(self):
		return {'anntations': [annotation.json() for annotation in AnnotModel.query.all()]}


class Annot(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('ref',
	type=int,
	)
	parser.add_argument('username',
	type=str,
	)
	parser.add_argument('judgement',
	type=int,
	)
	parser.add_argument('comment',
	type=str,
	)

	#add find_by_methods e.g., get edge by exposure
	
	#gets annotations by ref
	def get(self,ref):
		edge = AnnotModel.find_annots_by_ref(ref)
		if edge:
			return edge.json()
		return {'message': '{} not found in db'.format(ref)}, 404

	@jwt_required()
	def post(self, ref):
		if AnnotModel.find_annots_by_ref(ref):
			return {'message' : "An annotation with ref '{}' already exists.".format(ref)}, 400

		data = Annot.parser.parse_args()

		annot = AnnotModel(ref, data['username', 'judgement', 'comment'])
		
		try:
			annot.save_to_db()
		except:
			return {'message' : "An error occured inserting the annotation.".format(ref)}, 500

	#delete annotation by ref
	#@jwt_required()
	def delete(self, ref):
		annot = AnnotModel.find_annots_by_ref(ref)
		if annot:
			annot.delete_from_db()

		return {'message' : "Annotation deleted"}

	def put(self, ref):
		data = Annot.parser.parse_args()

		annotation = AnnotModel.find_annots_by_ref(ref)

		if annotation is None:
			annotation = AnnotModel(ref, data['username', 'judgement', 'comment'])
		else:
			annotation.judgement = data['judgement']
			annotation.save_to_db()
			annotation.comment = data['comment']
			annotation.save_to_db()

		return annotation.json()