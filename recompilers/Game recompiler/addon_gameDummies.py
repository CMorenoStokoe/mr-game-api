from addon_gameDummies_CDSdatafile import inCDS, CDS

class Model_GD():
        
    def gameDummies(nodeList,linkList):
        
        #0) Prep Custom/DefaultScoring lists and default values for non-listed nodes
        
        nodesForCustomScoring = inCDS
        count_CDSuse = 0
        
        defaultActivationValues = {
            'activation': 10,
            "activation_max" : 100,
            "activation_min" : 0,
            "negative" : "False",
            "units" : "Units",
            "units_type" : "float",
            "units_mapping" : None
        }
        count_default = 0
        
        #1) Add to nodes dummmy properties for game to use
        
        idToMrbaseIdDict = {}
        
        paddedNodes = []
        
        for node in nodeList:
            
            idToMrbaseIdDict[node["id"]]= node["id_MRBase"]
            
            if (node["id_MRBase"] in nodesForCustomScoring):
                activationValues = CDS[node["id_MRBase"]]
                count_CDSuse += 1
            else:
                activationValues = defaultActivationValues
                count_default += 1
            
            paddedNodes.append(
                {
                    'activation': activationValues['activation'], 
                    'group': node['group'], 
                    'id': node['id'], 
                    'shortName': node['shortName'], 
                    'grpColor': node['grpColor'],
                    "id_MRBase": node["id_MRBase"],
                    "activColor" : "white",
                    "currIntvLvl" : 0,
                    "totalFunds" : 0,
                    "iconId" : 'icons/'+node["id_MRBase"].replace(":", "")+'.png',
                    "activation_max" : activationValues['activation']*2,
                    "activation_min" : 0,
                    "negative" : activationValues["negative"],
                    "units" : activationValues["units"],
                    "units_type" : activationValues["units_type"],
                    "units_mapping" : activationValues["units_mapping"]
                }
            )
        
        dummyCount_nodes = len(paddedNodes[0])-6
        
        #2) Add to links dummmy properties for game to use
        
        paddedLinks = []
        
        for link in linkList:
            paddedLinks.append(
                {
                    'id': link['id'], 
                    'source': link['source'], 
                    'target': link['target'], 
                    'value': link['value'], 
                    'color': link['color'],
                    "currIntvLvl" : 0,
                    "source_iconId": 'icons/'+idToMrbaseIdDict[link["source"]].replace(":", "")+'.png',
                    "target_iconId": 'icons/'+idToMrbaseIdDict[link["target"]].replace(":", "")+'.png',
                }
                
            )
        
        
        dummyCount_links = len(paddedLinks[0])-5
            
        #messages
        
        messages=[
            "**:  {} game dummy properties added to nodes and {} added to links".format(dummyCount_nodes, dummyCount_links),
            "**:  Custom scoring paramaters found for {} nodes (mode: Auto min/max). Succesfully configured {} nodes. {} remaining nodes default".format(len(inCDS), count_CDSuse, count_default)
        ]
        
        return (paddedNodes, paddedLinks, messages)
