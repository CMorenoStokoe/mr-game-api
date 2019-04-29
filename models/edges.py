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
		self.annotations = annotations

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
	def find_edges_by_expName(cls, exp_name):
		return [edge.json() for edge in EdgeModel.query.filter_by(exp_name=exp_name).all()]

	@classmethod
	def expName_to_ref(cls, exp_name):
		edge = EdgeModel.query.filter_by(exp_name=exp_name).first()
		return edge.ref
	
	@classmethod
	def expNameAndOutName_to_ref(cls, exp_name,out_name):
		edge = EdgeModel.query.filter_by(exp_name=exp_name).filter_by(out_name=out_name).first()
		return edge.ref

	@classmethod
	def find_edge_by_expNameAndOutName(cls, exp_name, out_name):
		edge = EdgeModel.query.filter_by(exp_name=exp_name).filter_by(out_name=out_name).first()
		return {"edges" : edge.json()}

	#add method to intialise
	#@classmethod
	#def initialise(cls,ref)
		#edge = find_edges_by_ref(ref)
		#edge.annotations = 'annotations':[]
		#edge.save_to_db()