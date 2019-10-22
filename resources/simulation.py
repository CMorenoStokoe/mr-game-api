#Import
from flask_restful import Resource #REST API resources 
import json # Handling json objects
from flask_restful import reqparse

from models.simulation import *
from startup.init import Start_Values
from models.simulation import Propagation
from models.views import Collapse_Groups

class View_Data(Resource):
    def get(self):
        with open('models/data.json') as json_file:    
            data = json.load(json_file)
        
        #Views
        view="collapsed"
        #set values (test -- revise)
        if view == "collapsed":
            dataview = Collapse_Groups(data["nodes"],data["links"])
            print(dataview[2],dataview[3])
            return {"nodes":dataview[0], "links":dataview[1]}
        elif view == "normal":
            return data 
        elif view == "node":
            return data

class View_Node(Resource):
    def get(self, node):
        with open('models/data.json') as json_file:    
            data = json.load(json_file)
        spottedLinks = [i for i in data["links"] if i["source"]==node or i["target"]==node]
        nodeList0 = [i["target"] for i in data["links"] if i["source"]==node or i["target"]==node]
        nodeList1 = [i["source"] for i in data["links"] if i["source"]==node or i["target"]==node]
        nodeList=[]
        nodeList.append(node)
        for node in nodeList0:
            if node not in nodeList:
                nodeList.append(node)
        for node in nodeList1:
            if node not in nodeList:
                nodeList.append(node)       
        spottedNodes = [i for i in data["nodes"] if i["id"] in nodeList]
        spotted = ({"nodes":spottedNodes,"links":spottedLinks})
        print(spotted)
        return spotted
        
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