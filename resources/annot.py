from db import db
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.annot import AnnotModel
from models.edges import EdgeModel
from db import db

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
    def post(self, exp_name, out_name):
        data = Annots.parser.parse_args()

        ref = EdgeModel.expNameAndOutName_to_ref(exp_name, out_name)
        username = data['username']

        annotExists = AnnotModel.find_annots_by_refAndUsr(ref, username) 
        if annotExists:
            return {"Message": "Annotation already made by user {}, please use PUT to update instead".format(username), 'Existing annotation': annotExists}, 303
        newAnnot = AnnotModel(
                                None, 
                                ref, 
                                data['username'], 
                                data['judgement'], 
                                data['comment']
                        )
        newAnnot.save_to_db()
        return {'Message': "Annotation made successfully", 'Preview': newAnnot.json()}, 201

    def put(self, exp_name, out_name):
        data = Annots.parser.parse_args()

        ref =  EdgeModel.expNameAndOutName_to_ref(exp_name, out_name)
        username = data['username']
        
        findAnnotID = AnnotModel.find_annotID_by_refAndUsr(ref, username)
        intAnnotID = int(findAnnotID)
        return AnnotModel.update_annots_by_annotID(intAnnotID), 201

    
class AnnotDel(Resource):
    
    def delete(self, exp_name, out_name, username):
        
        ref = EdgeModel.expNameAndOutName_to_ref(exp_name, out_name)
        
        annot = AnnotModel.find_annots_by_refAndUsr(ref, username)
        if annot:
            db.session.delete(annot)
            db.session.commit()
            return annot.json()
        return {'message': " Comment by {} on this edge not found in db".format(username)}, 404