#Import
import requests #HTML requests
from flask import jsonify #Returning JSON
import json
import os
import networkx as nx #Network graph
from networkx import json_graph
from algorithms.propagation import propagate

#Debug options
debug_api_changeValues = True


#Models callable by resources

def Overall_Stats(goalId, goalValue):
    OverallActivation = 0
    GoalActivation = 0
    with open('models/data.json', 'r') as json_file:
        dat = json.load(json_file)
        for node in dat["nodes"]:
            OverallActivation += node["activation"]
            if node["id"] == goalId:
                GoalActivation = node["activation"]
        if OverallActivation > 2300:
            OverallActivation = 2300
        elif OverallActivation < 0:
            OverallActivation = 0
        OverallHealth = 2300-OverallActivation
        OH_sliderVal = OverallHealth/2300*100 #FIX SO ACCURATE
        if OH_sliderVal > 100:
            OH_sliderVal = 100
        elif OH_sliderVal < 0:
            OH_sliderVal = 0
        GoalHealth = GoalActivation/goalValue*100 #FIX SO ACCURATE
    return(str(OverallHealth), goalId, str(GoalHealth), str(OH_sliderVal))

def Change_Values(intervention):
    
    #Debug console            
    if debug_api_changeValues == True:
        print("debug_api_changeValues: Change values method called with payload {} ".format(intervention))
      
    #Parse args create dummy variables for assignment
    nodeID=intervention["id"]
    intvValence=intervention["valence"]
    intvValue=intervention["value"]
    recompiledNodes = []
    recompiledLinks = []
    
    #Read data
    with open('models/data.json', 'r') as json_file:
        dat = json.load(json_file)
        
        #Change nodes
        for node in dat["nodes"]:
            
            if node["id"] == nodeID:
                nodeAct_init=node["activation"]
                
                if node["activation"] == node["activation_max"] or node["activation"] == node["activation_min"] :
                    return(999) #Return code 999 (value at maximum/minimum)
                
                #Update node activation stats
                intervention_value = intervention["value"]
                
                if intvValence == "+":
                    activationAfterIntervention = node["activation"] + intervention_value
                    node["activation"] = DynamicallyRoundValue(activationAfterIntervention)
                    node["currIntvLvl"] = intvValue
                    node["totalFunds"] += (intvValue)*1000
                    if (activationAfterIntervention > node["activation_max"]):
                        newVal = node["activation_max"]
                    else:
                        newVal=DynamicallyRoundValue(activationAfterIntervention)
                elif intvValence == "-":
                    activationAfterIntervention = node["activation"] - intervention_value
                    node["currIntvLvl"] = 0-(intvValue)
                    node["totalFunds"] += (intvValue)*1000
                    if (activationAfterIntervention < node["activation_min"]):
                        newVal = node["activation_min"]
                    else:
                        newVal=DynamicallyRoundValue(activationAfterIntervention)
                    
                if debug_api_changeValues == True: 
                    print("debug_api_changeValues: Intervention: {} ({}-->{})".format(node["id"],nodeAct_init, node["activation"]))
                
            recompiledNodes.append(node)
            
    changedDat = {"nodes":recompiledNodes, "links":dat["links"]}
    
    #Write changes to data file
    with open('models/data.json', 'w') as json_file:
        json.dump(changedDat, json_file, indent=4, sort_keys=True)
    
    return(newVal)
        
def Propagation(intervention, newVal):
    nodeID=intervention["id"]
    intvValence=intervention["valence"]
    intvValue= newVal #Pass through updated node value from change_values
    recompiledNodes=[]
    
    #Init HealthG
    json_graph_data = os.path.join('models', 'data.json')
    graph_data = json.load(open(json_graph_data))
    HealthG = nx.DiGraph()
    nodes = graph_data['nodes']
    node_ids = [n['id'] for n in nodes]
    node_ids_map = {k:v for k, v in zip(node_ids, range(len(node_ids)))}
    HealthG.add_nodes_from((node['id'], node) for node in nodes)
    edges = graph_data['links']
    HealthG.add_edges_from([(edge['source'], edge['target'], {k:v for k,v in edge.items() }) for edge in edges])
    
    #Propagate
    propDict = propagate(HealthG, nodeID, intvValue)
    
    nx.set_node_attributes(HealthG, propDict)
    export_json = nx.json_graph.node_link_data(HealthG)
    json.dump(export_json, open('models/data.json', 'w'))
    
#    with open('models/data.json', 'r+') as json_file:
#        dat = json.load(json_file) 
#        for node in dat["nodes"]:
#            node["activation"]=propDict[node["id"]]
#            print(node["id"],node["activation"])
#        json.dump(dat, json_file, indent=4, sort_keys=True)

    return('{}(->{})'.format(intervention["id"],round(newVal,2)))

def CleanData():
    
    recompiledNodes = []
    
    with open('models/data.json', 'r') as json_file:
        dat = json.load(json_file)
        
        #Change nodes
        for node in dat["nodes"]:
                
            #Colour nodes 
            activation_pct = node["activation"]/node["activation_max"]*100
            activation_pct_rd = DynamicallyRoundValue(activation_pct)
            if activation_pct < 50:
                node["activColor"] = "rgba(25, 25, 240, {})".format(100-activation_pct_rd/100)
                if debug_api_changeValues == True: 
                    print("debug_api_changeValues: Node coloured: {} : {})".format(node["id"], node["activColor"]))
            elif activation_pct == 50:
                node["activColor"] = "white"
                if debug_api_changeValues == True: 
                    print("debug_api_changeValues: Node coloured: {} : {})".format(node["id"], node["activColor"]))
            else:
                node["activColor"] = "rgba(240, 25, 25, {})".format(activation_pct_rd/100)
                if debug_api_changeValues == True: 
                    print("debug_api_changeValues: Node coloured: {} : {})".format(node["id"], node["activColor"]))
            
            #Round activations
            activation = node['activation']
            node['activation'] = DynamicallyRoundValue(activation)
            
            #Cap min/max (crude retro capping, reduces simulation accuracy while propagation model still does not respect min/max)
            if activation > node['activation_max']:
                node['activation'] = node['activation_max']
            elif activation < node["activation_min"]:
                node['activation'] = node["activation_min"]
                
            recompiledNodes.append(node)
            
    changedDat = {"nodes":recompiledNodes, "links":dat["links"]}
    
    #Write changes to data file
    with open('models/data.json', 'w') as json_file:
        json.dump(changedDat, json_file, indent=4, sort_keys=True)
        
    return()

def DynamicallyRoundValue(value):
    if (value >=100):
        return round(value, 0)
    elif (value >=1):
        return round(value, 1)
    elif (value >=0.1):
        return round(value, 2)
    elif (value >=0.01):
        return round(value, 3)
    elif (value >=0.001):
        return round(value, 4)
    else:
        return round(value, 5)