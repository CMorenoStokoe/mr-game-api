from db import db

class AnnotModel(db.Model):
	__tablename__ = 'annotations'

	annotID = db.Column(db.Integer, primary_key=True)
	ref = db.Column(db.Integer, db.ForeignKey('edges.ref'))
	username = db.Column(db.String(80))
	judgement = db.Column(db.Integer)
	comment = db.Column(db.String(999))

	edge = db.relationship('EdgeModel')

	def __init__(self, ref, username, judgement, comment):
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
		return cls.query.filter_by(ref=ref).first()

	#add find_by methods for each relevant paramater

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
		return {'request_success':"Data saved successfully"}

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()