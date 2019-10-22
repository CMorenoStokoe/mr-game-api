#Import
import requests #HTML requests
from flask import jsonify #Returning JSON
import json
import os
import networkx as nx #Network graph
from networkx import json_graph
from algorithms.propagation import propagate

#from models.data import data


def Change_Values(directive):
    nodeID=directive["id"]
    intvValence=directive["valence"]
    intvValue=directive["value"]
    recompiledNodes = []
    with open('models/data.json', 'r') as json_file:
        dat = json.load(json_file)
        for node in dat["nodes"]:
            if node["id"] == nodeID:
                nodeAct_init=node["activation"]
                if intvValence == "+":
                    node["activation"] += intvValue
                    newVal=node["activation"]
                elif intvValence == "-":
                    node["activation"] -= intvValue
                    newVal=node["activation"]
                print("Intervention: {} ({}-->{})".format(node["id"],nodeAct_init, node["activation"]))
            recompiledNodes.append(node)
    changedDat = {"nodes":recompiledNodes, "links":dat["links"]}
    with open('models/data.json', 'w') as json_file:
        json.dump(changedDat, json_file, indent=4, sort_keys=True)
    return(newVal)

        
def Propagation(directive, newVal):
    nodeID=directive["id"]
    intvValence=directive["valence"]
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
        
    print("Intervention effects propagated through network: ",directive,newVal)