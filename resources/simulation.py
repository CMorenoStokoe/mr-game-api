#Import
from flask_restful import Resource #REST API resources 
import json # Handling json objects
from models.simulation import * #Import all models in the simulation file
from flask_restful import reqparse

class View_Data(Resource):
     def get(self):
        with open('models/data.json') as json_file:
            return json.load(json_file)
    
class Intervene(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id cannot be converted')
        args = parser.parse_args() 
        print(args)
        Change_Values(args.id)