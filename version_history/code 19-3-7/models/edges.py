import sqlite3
from db import db

class EdgeModel(db.Model):
	__tablename__ = 'edges'

	ref = db.Column(db.Integer, primary_key=True)
	exposure = db.Column(db.Integer)
	exp_name = db.Column(db.String(80))
	outcome = db.Column(db.Integer)
	out_name = db.Column(db.String(80))
	MRestimate = db.Column(db.Float(precision=10))

	def __init__(self, ref, exposure, exp_name, outcome, out_name, MRestimate):
		self.ref = ref
		self.exposure = exposure
		self.exp_name = exp_name
		self.outcome = outcome
		self.out_name = out_name
		self.MRestimate = MRestimate

	def json(self):
		return {
					'ref': self.ref,
					'exposure': self.exposure, 
					'exp_name': self.exp_name,
					'outcome': self.outcome,
					'out_name': self.out_name,
					'MRestimate': self.MRestimate
				}


	@classmethod
	def find_edges_by_ref(cls, ref):

		connection = sqlite3.connect('edgedb.db')
		cursor = connection.cursor()

		query = "SELECT * FROM edges where ref=?"
		result = cursor.execute(query, (ref,))
		all_rows = result.fetchone()
		connection.close()

		if all_rows:
			return cls(*all_rows)
		
class AnnotModel(db.Model):
	__tablename__ = 'annotations'

	annotID = db.Column(db.Integer, primary_key=True)
	ref = db.Column(db.Integer)
	username = db.Column(db.String(80))
	judgement = db.Column(db.Integer)
	comment = db.Column(db.String(999))

	def __init__(self, annotID, ref, username, judgement, comment):
		self.annotID = annotID
		self.ref = ref
		self.username = username
		self.judgement = judgement
		self.comment = comment

	def json(self):
		return {
					'annotID': self.annotID,
					'ref': self.ref, 
					'username': self.username,
					'judgement': self.judgement,
					'comment': self.comment
				}

	@classmethod
	def find_annots_by_ref(cls, ref):
		connection = sqlite3.connect('annotdb.db')
		cursor = connection.cursor()

		query = "SELECT * FROM annotations where ref=?"
		result = cursor.execute(query, (ref,))
		all_rows = result.fetchone()
		connection.close()

		if all_rows:
			return cls(*all_rows)

	#move annotmodel to seperate file
	#add find_by methods for each relevant paramater

	def insert(self):
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
