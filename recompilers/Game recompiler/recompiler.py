#0) Initialise

print("***Start***")

import json 
import os.path 

#Detect addons
from options import *

ao_exclusionCriteria = os.path.exists("addon_exclusionCriteria.py")
if (ao_exclusionCriteria==True):
    from addon_exclusionCriteria import Model_EC
ao_selectedNodes = os.path.exists("addon_selectedNodes.py")
if (ao_selectedNodes==True):
    from addon_selectedNodes import Model_SN
ao_collapsedGroups = os.path.exists("addon_collapsedGroups.py")
if (ao_collapsedGroups==True):
    from addon_collapsedGroups import Model_CG
ao_linkCount = os.path.exists("addon_linkCount.py")
if (ao_linkCount==True):
    from addon_linkCount import Model_LC
ao_coloredGroups = os.path.exists("addon_coloredGroups.py")
if (ao_coloredGroups==True):
    from addon_coloredGroups import Model_ClG
ao_gameDummies = os.path.exists("addon_gameDummies.py")
if (ao_gameDummies==True):
    from addon_gameDummies import Model_GD
    
#import original JSON file as object
with open('MRNV_output.json') as json_file:
    data = json.load(json_file)

print("*: 20% Complete - Original data read and selected ***")


#1 & 2) Recompile nodes into d3-readable array & populate ID:name mapping dictionary & then Recompile edges into de3-readable format

recompiledNodes = []
dictID = {}
recompiledEdges = []

if jsonFormat == 'PD4HH':
    
    #select the data as it is specified in the original JSON
    selector1 = data["goals"]
    selector2 = data["policies"]
    #set counter for incrementing IDs
    counter=1
    
    #Nodes
    for node in selector1:#iterates over 'goals'
        dictID[node["id"]]=node["name"]
        recompiledNodes.append(
            {
                "id":node["name"],
                "activation":default_node_activation,
                "group":node["group"],
                "shortName":node["short_name"]
            }
        )
    for node in selector2:#iterates over 'policies'
        dictID[node["id"]]=node["name"]
        recompiledNodes.append(
            {
                "id":node["name"],
                "activation":default_node_activation,
                "group":node["group"],
                "shortName":node["short_name"]
            }
        )
        
    #Links
    for node in selector1:#iterates over 'goals'
        for edge in node["connections"]:
            edgefID = edge["from_id"]
            edgetID = edge["to_id"]
            edgeWeight = edge["weight"]
            edgefName = dictID[edgefID]
            edgetName = dictID[edgetID]

            if (edgeWeight >= 0):
                edgeColor = "red"
            else:
                edgeColor = "blue"

            recompiledEdges.append(
                {
                    "id":counter,
                    "source":edgefName,
                    "target":edgetName,
                    "value":edgeWeight,
                    "color":edgeColor
                }
            )
            counter+=1
    for node in selector2:#iterates over 'policies'
        for edge in node["connections"]:
            edgefID = edge["from_id"]
            edgetID = edge["to_id"]
            edgeWeight = edge["weight"]
            edgefName = dictID[edgefID]
            edgetName = dictID[edgetID]

            if (edgeWeight >= 0):
                edgeColor = "red"
            else:
                edgeColor = "blue"

            recompiledEdges.append(
                {
                    "id":counter,
                    "source":edgefName,
                    "target":edgetName,
                    "value":edgeWeight,
                    "color":edgeColor
                }
            )
            counter+=1

if jsonFormat == 'MRNV':
    
    #Nodes
    for node in data['nodes']:
        dictID[node["id"]]=node["name"]
        recompiledNodes.append(
            {
                "id":node["name"],
                "activation":default_node_activation,
                "group":node["group"],
                "shortName":node["short_name"]
            }
        )
    
    #Links
    for edge in data['links']:
        edgefID = edge["source"]
        edgetID = edge["target"]
        edgeWeight = edge["b"]
        edgeColor = edge["color"]
        edgeId = edge["id"]
        edgefName = dictID[edgefID]
        edgetName = dictID[edgetID]

        recompiledEdges.append(
            {
                "id":edgeId,
                "source":edgefName,
                "target":edgetName,
                "value":edgeWeight,
                "color":edgeColor
            }
        )
        
print("*: 50% complete - Vanilla dataset recompiled ***")           
        
        
#3) Perform select addon operations

#Exclude certain nodes
if (ao_exclusionCriteria==True):
    EC = Model_EC.exclusionCriteria(recompiledNodes, recompiledEdges, excluded_nodes)
    recompiledNodes=EC[0]
    recompiledEdges=EC[1]
    print(EC[2])
#Select only certain nodes
if (ao_selectedNodes==True):
    SN = Model_SN.selectedNodes(recompiledNodes, recompiledEdges, selected_nodes)
    recompiledNodes=SN[0]
    recompiledEdges=SN[1]
    print(SN[2])
#Add nodes representing groups in data
if (ao_collapsedGroups==True):
    if collapse_all_groups==True:
        CG = Model_CG.collapsedGroups(recompiledNodes, recompiledEdges)
        recompiledNodes=CG[0]
        recompiledEdges=CG[1]
        print(CG[2])
        print(CG[3])
#Add count of links per node (used in ordering GUI)
if (ao_linkCount==True):
    if count_links_per_node == True:
        LC = Model_LC.linkCount(recompiledEdges)
        for count in LC[1]:
            print(count['count']," : ",count['node'])
#Add colours to groups
if (ao_coloredGroups==True):
    ClG = Model_ClG.coloredGroups(recompiledNodes,colorScheme)
    recompiledNodes=ClG[0]
    print(ClG[1])
#Add dummy poperties for game use
if (ao_gameDummies==True):
    GD = Model_GD.gameDummies(recompiledNodes, recompiledEdges)
    recompiledNodes=GD[0]
    recompiledEdges=GD[1]
    print(GD[2])

print("*: 80% complete - Addon dataset recompiled ***")
    
#4) Write d3-ready JSON file

recompiledJson = {"nodes":recompiledNodes, "links":recompiledEdges}
    
print("***End***")

with open('../../startup/MRG_output.json', 'w') as json_file:
    json.dump(recompiledJson, json_file, indent=4, sort_keys=True)