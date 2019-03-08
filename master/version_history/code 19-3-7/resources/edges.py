import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.edges import EdgeModel, AnnotModel

	#get status (debug)
class Status(Resource):
	def get(self):
		return 'OK', 200


	#get list of edges
class View(Resource):
	def get(self, database):
		if database == "edges":
			connection = sqlite3.connect('edgedb.db')
			cursor = connection.cursor()

			query = "SELECT * FROM edges"
			result = cursor.execute(query)
			all_rows = result.fetchall()

			return all_rows #replace with method to retun dicts

			#for row in all_rows:
			#	return{
			#					'ref':row[0], 
			#					'exposure':row[1], 
			#					'exp_name':row[2], 
			#					'outcome':row[3], 
			#					'out_name':row[4], 
			#					'MRestimate':row[5],								
			#	}

			connection.close ()

		elif database == "annotations":
			connection = sqlite3.connect('annotdb.db')
			cursor = connection.cursor()

			query = "SELECT * FROM annotations"
			result = cursor.execute(query)
			all_rows = result.fetchall()
			
			return all_rows

			#	return{
			#			'edge':{
			#					'annotID':row[0], 
			#					'ref':row[1], 
			#					'username':row[2], 
			#					'judgement':row[3], 
			#					'comment':row[4], 
			#					}
			#	}

			connection.close ()

		else:
			return {'message':'Database {} not found'.format(database)}, 404


class Edge(Resource):

	#get edge by exposure
	def get(self,ref):
		edge = EdgeModel.find_edges_by_ref(ref)
		if edge:
			return edge.json()
		return {'message': '{} not found in db'.format(ref)}, 404


class Annotation(Resource):

	#add find_by_methods

	#get annotations by ref
		#get edge by exposure
	def get(self,ref):
		edge = AnnotModel.find_annots_by_ref(ref)
		if edge:
			return edge.json()
		return {'message': '{} not found in db'.format(ref)}, 404

	#delete annotation by ref
	#@jwt_required()
	def delete(self, annotID):
		connection = sqlite3.connect('annotdb.db')
		cursor = connection.cursor()

		query = "DELETE FROM annotations WHERE annotID=?"
		cursor.execute(query, (annotID,))

		connection.commit()
		connection.close()

		return {'message':'Item deleted'}


class Annotate(Resource):

	#add try, except error catching
	#add dedicated post method to search for existing annotations

	#put (update/create) new annotation (CURRENTLY)
	@jwt_required()
	def put(self):
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

		connection = sqlite3.connect('annotdb.db')
		cursor = connection.cursor()

		data=parser.parse_args()

		insert_query = "INSERT INTO annotations VALUES (NULL, ?, ?, ?, ?)"

		annotation = (data['ref'], data['username'], data['judgement'], data['comment'])
		cursor.execute(insert_query, annotation)

		connection.commit()
		connection.close()

		return {'request_success_preview':data}, 202