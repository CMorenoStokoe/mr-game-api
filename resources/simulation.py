#Import
from flask_restful import Resource #REST API resources 
import json # Handling json objects
from flask_restful import reqparse

from models.simulation import *
from startup.init import Start_Values, Start_Buttons
from models.simulation import Propagation, Overall_Stats
from models.views import Collapse_Groups

#Debug console
debug_api_viewNode = False
debug_api_intervene = False


#Available methods callable as resources
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
        
        #Compile nodes/links
        spotted = ({"nodes":spottedNodes,"links":spottedLinks})
        
        #Debug
        if debug_api_viewNode == True:
            print("debug_api_viewNode: viewNode called with target node ID {}".format(centerNode))
            print("debug_api_viewNode: target node ID added to nodelist : {}".format(nodeList))
            print("debug_api_viewNode: Accessed data.json ({} nodes, {} links) ".format(len(data['nodes']),len(data['links'])))
            print("debug_api_viewNode: Spotted and obtained links related to target node: ", spottedLinks)
            print("debug_api_viewNode: Built list of IDs for nodes related to target node ", nodeList)
            print("debug_api_viewNode: Spotted and obtained nodes related to target node: ", spottedNodes)
            print("debug_api_viewNode: Combined nodes and links for return: ", spotted)
        
        #Return nodes/links for view
        print("INFO: Viewing: "+centerNode)
        return spotted
        
class Intervene(Resource):
    
    currentInterventions = {}
    
    def get(self):
        
        #Method called when there is no new intervention but another tick of further simulating existing intervention effects has been requested
        
        interventionLog = []
        for intervention in self.currentInterventions:
            newVal=Change_Values(self.currentInterventions[intervention])
            interventionLog.append(Propagation(self.currentInterventions[intervention],newVal))
        
        print("*Tick* Propagation :", interventionLog)
        
    def post(self):
        
        #Parse posted json file
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id cannot be converted')
        parser.add_argument('valence', type=str, help='valence cannot be converted')
        parser.add_argument('value', type=int, help='value cannot be converted')
        newIntervention = parser.parse_args() 
        
        #Save interventions to list of current interventions if intervention level != 0
        if newIntervention['value'] != 0:
            self.currentInterventions[newIntervention['id']]={
                'id' : newIntervention['id'],
                'valence' : newIntervention['valence'],
                'value' : newIntervention['value']
            }
        #Remove intervention from memory if intervention level == 0
        elif newIntervention['value'] == 0:
            self.currentInterventions.pop(newIntervention['id'])
        
        if debug_api_intervene == True:
            print("debug_api_intervene: New intervention information parsed: {}".format(newIntervention))
            print("debug_api_intervene: Intervention list saved to memory: {}".format(self.currentInterventions))
        
        interventionLog = []
        for intervention in self.currentInterventions:
            newVal=Change_Values(self.currentInterventions[intervention])
            interventionLog.append(Propagation(self.currentInterventions[intervention],newVal))
        
        print("Interventions propagated :", interventionLog)
    
class Update(Resource):
    def get(self):
        with open('models/data.json', 'r') as json_file:    
            data = json.load(json_file)
        stats = Overall_Stats("Subjective well being",100)
        groups = Start_Buttons()
        return ({"nodes":data["nodes"],"stats":stats,"groups":groups["groups"]})
        
class Reset(Resource):
    def get(self):
        Start_Values()