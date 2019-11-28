#Import
from flask_restful import Resource #REST API resources 
import json # Handling json objects
from flask_restful import reqparse

from models.simulation import *
from startup.init import Start_Values, Start_Buttons
from models.simulation import Propagation, Overall_Stats
from models.views import Collapse_Groups

class Stats(Resource):
    def get(self):
        return(Overall_Stats())
    
class View_Data(Resource):
    def get(self):
        with open('models/data.json', 'r') as json_file:    
            data = json.load(json_file)
        
        #Views
        view="normal"
        #set values (test -- revise)
        if view == "collapsed":
            dataview = Collapse_Groups(data["nodes"],data["links"])
            return {"nodes":dataview[0], "links":dataview[1]}
        elif view == "normal":
            return data 
        elif view == "node":
            return data
        elif view == "activeLinks":
            return data

class View_DataNormal(Resource):
    def get(self):
        with open('models/data.json', 'r') as json_file:    
            data = json.load(json_file)
        return data

class View_Node(Resource):
    def get(self, centerNode):
        with open('models/data.json') as json_file:    
            data = json.load(json_file)
        
        #Get relevant links
        spottedLinks = [i for i in data["links"] if i["source"]==centerNode or i["target"]==centerNode]
        nodeList0 = [i["target"] for i in data["links"] if i["source"]==centerNode or i["target"]==centerNode]
        nodeList1 = [i["source"] for i in data["links"] if i["source"]==centerNode or i["target"]==centerNode]
        
        #Get relevant node IDs
        nodeList=[]
        nodeList.append(centerNode)
        for node in nodeList0:
            if node not in nodeList:
                nodeList.append(node)
        for node in nodeList1:
            if node not in nodeList:
                nodeList.append(node)   
        #Get relevant nodes
        #nodeList.remove(centerNode) CURRENTLY DISABLED (see blw)
        spottedNodes = [i for i in data["nodes"] if i["id"] in nodeList]
        
        #CURRENTLY DISABLED Change centerNode (target node) to be more visible
#        for node in data["nodes"]:
#            if node["id"] == centerNode:
#                spottedNodes.append(
#                                       {
#                                           "id":node["id"],
#                                           "group":node["group"],
#                                           "activation":node["activation"],
#                                           "grpColor":node["activation"],
#                                           "shortName":node["activation"]
#                                       }
#                )
#                
        #Compile and return nodes/links for view
        spotted = ({"nodes":spottedNodes,"links":spottedLinks})
        print("Viewing: "+centerNode)
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
    
class Update(Resource):
    def get(self):
        with open('models/data.json', 'r') as json_file:    
            data = json.load(json_file)
        stats = Overall_Stats("Intracranial volume",100)
        groups = Start_Buttons()
        return ({"nodes":data["nodes"],"stats":stats,"groups":groups["groups"]})
        
class Reset(Resource):
    def get(self):
        Start_Values()