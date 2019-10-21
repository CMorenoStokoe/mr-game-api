#Import
from flask_restful import Resource #REST API resources 
import json # Handling json objects
from flask_restful import reqparse

from models.simulation import *
from startup.init import Start_Values
from models.simulation import Propagation

class View_Data(Resource):
     def get(self):
        with open('models/data.json') as json_file:
            return json.load(json_file)
        
class Intervene(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id cannot be converted')
        parser.add_argument('valence', type=str, help='valence cannot be converted')
        parser.add_argument('value', type=int, help='value cannot be converted')
        directive = parser.parse_args() 
        print("Intervention! : ", directive)
        newVal=Change_Values(directive)
        Propagation(directive,newVal)
        
class Reset(Resource):
    def get(self):
        Start_Values()