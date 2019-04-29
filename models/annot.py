from db import db
from flask_restful import reqparse
from models.edges import EdgeModel

class AnnotModel(db.Model):
    __tablename__ = 'annotations'

    annotID = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.Integer, db.ForeignKey('edges.ref'))
    username = db.Column(db.String(80))
    judgement = db.Column(db.Integer)
    comment = db.Column(db.String(999))

    edge = db.relationship('EdgeModel')

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

    
    @classmethod
    def find_annots_by_expName(cls, exp_name):
        ref = EdgeModel.expName_to_ref(exp_name)
        annots = [edge.json() for edge in AnnotModel.query.filter_by(ref=ref).all()]
        if annots:
            return {exp_name: annots}
        return {'message': '{} not found in db'.format(exp_name)}, 404
    
    @classmethod
    def find_annots_by_refAndUsr(cls, ref, username):
        annots = cls.query.filter_by(ref=ref).filter_by(username=username).first()
        if annots:
            return annots
        return None
    
    @classmethod
    def find_annotID_by_refAndUsr(cls, ref, username):
        annots = cls.query.filter_by(ref=ref).filter_by(username=username).first()
        if annots:
            return annots.annotID
        return None
    
    @classmethod
    def update_annots_by_annotID(cls, annotID):
        data = cls.parser.parse_args()
        
        annot = cls.query.filter_by(annotID=annotID).first()

        if annot:
            origAnnot = annot.json()
            annot.judgement = data['judgement']
            annot.save_to_db()
            annot.comment = data['comment']
            annot.save_to_db()
            newAnnot = annot
            return {'Message': "Annotation updated successfully", 'Old annotation': origAnnot, 'Updated to': newAnnot.json()}, 200
        return {'Message': "Annotation not already made by user {}, please use POST to create instead".format(username)}, 404
        
        
    #add find_by methods for each relevant paramater

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return {'request_success':"Data saved successfully"}
    
    @classmethod
    def delete_from_db(cls):
        db.session.delete(cls)
        db.session.commit()