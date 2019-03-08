from db import db

class EdgeModel(db.Model):
	__tablename__ = 'edges'

	ref = db.Column(db.Integer, primary_key=True)
	exposure = db.Column(db.Integer)
	exp_name = db.Column(db.String(80))
	outcome = db.Column(db.Integer)
	out_name = db.Column(db.String(80))
	MRestimate = db.Column(db.Float(precision=10))

	annotations = db.relationship('AnnotModel', lazy='dynamic')

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
					'MRestimate': self.MRestimate,
					'annotations': [annot.json() for annot in self.annotations.all()]
				}

	@classmethod
	def find_edges_by_ref(cls, ref):
		return cls.query.filter_by(ref=ref).first()