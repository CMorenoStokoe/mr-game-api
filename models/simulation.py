#Import
import requests #HTML requests
from flask import jsonify #Returning JSON
import json


def Change_Values(args):
    nodeID=args["id"]
    intvValence=args["valence"]
    intvValue=args["value"]
    recompiledNodes = []
    with open('models/data.json') as json_file:
        dat = json.load(json_file)
        for node in dat["nodes"]:
            if node["id"] == nodeID:
                nodeAct_init=node["activation"]
                if intvValence == "+":
                    node["activation"] += intvValue
                elif intvValence == "-":
                    node["activation"] -= intvValue
                print("Intervention: {} ({}-->{})".format(node["id"],nodeAct_init, node["activation"]))
            recompiledNodes.append(node)
    changedDat = {"nodes":recompiledNodes, "links":dat["links"]}
    with open('models/data.json', 'w') as json_file:
        json.dump(changedDat, json_file, indent=4, sort_keys=True)

def Propagation(param):
    pass #convert javascript function to python