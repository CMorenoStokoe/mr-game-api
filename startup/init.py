#Import
import json #converting json objects in python
import networkx as nx #All for network graph data startup
from typing import Dict, Callable, List, Set, Sequence, Tuple
from collections import defaultdict
import os

from models.simulation import Change_Values, Propagation

#from models.data import data

def Start_Values(): #make copy of original start data
    with open("startup/playable_health_v6.json", "r") as json_file:
        dat = json.load(json_file) 

    # Pre-propagate - add me here (currently doesn't work because propagation gives different values depending on the path taken) 
        
    with open("models/data.json", "w") as json_file:
        json.dump(dat, json_file, indent=4, sort_keys=True)    
        
def Start_Buttons():
    nodeGroups = []
    btnDict = []
    colors = {}
    
    with open('models/data.json') as json_file:
        data = json.load(json_file)
    
    #Dicts for group activation colors
    groupPrevs={}
    groupPrevCols={}
    #Identify nodes & build dictionary for groups' colors & activation colors
    for node in data["nodes"]:
        if node["group"] not in nodeGroups:
            nodeGroups.append(node["group"])
            colors[node["group"]]=node["grpColor"]
            groupPrevs[node["group"]]=node["activation"]
        elif node["group"] in nodeGroups:
            groupPrevs[node["group"]]+=node["activation"]
    
    #Colour groups according to activation
    for group in groupPrevs: 
        transparency = groupPrevs[group]/100
        if transparency > 100:
            transparency = 100
        elif transparency < 0:
            transparency = 0
        color = "rgba(240, 25, 25, {})".format(transparency)
        groupPrevCols[group] = color
        
    #Format node list for grouping buttons
    for group in nodeGroups:
        nodesInGroup=[]
        for node in data["nodes"]:
            if node["group"]==group:
                nodesInGroup.append(node)
        btnDict.append({"group":group,"nodes":nodesInGroup,"length":len(nodesInGroup),"grpColor":colors[group],"activColor":groupPrevCols[group],"activation":groupPrevs[group]})
        nodesInGroup = sorted(btnDict, key=lambda k: k['length'], reverse=True)
    return ({"groups":nodesInGroup})