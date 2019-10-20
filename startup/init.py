#Import
import json #converting json objects in python

def Start_Values(): #make copy of original start data
    with open("startup/playable_health_v5.json", "r") as json_file:
        dat = json.load(json_file)
    with open("models/data.json", "w") as json_file:
        json.dump(dat, json_file, indent=4, sort_keys=True)
        
def Start_Buttons():
    nodeGroups = []
    btnDict = []
    colors={}
    
    with open('models/data.json') as json_file:
        data = json.load(json_file)
    
    #Identify nodes & build dictionary for groups' colors
    for node in data["nodes"]:
        if node["group"] not in nodeGroups:
            nodeGroups.append(node["group"])
            colors[node["group"]]=node["grpColor"]
    
    #Format node list for grouping buttons
    for group in nodeGroups:
        nodesInGroup=[]
        for node in data["nodes"]:
            if node["group"]==group:
                nodesInGroup.append(
                        {
                            "id":node["id"],
                            "shortName":node["shortName"],
                            "group":node["group"]
                        }
                )
        btnDict.append({"group":group,"nodes":nodesInGroup,"length":len(nodesInGroup),"grpColor":colors[group]})
        nodesInGroup = sorted(btnDict, key=lambda k: k['length'])
    return ({"groups":nodesInGroup})
        