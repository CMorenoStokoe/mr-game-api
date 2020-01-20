class Model_GD():
        
    def gameDummies(nodeList,linkList):
        
        #1) Add to nodes dummmy properties for game to use
        
        paddedNodes = []
        
        for node in nodeList:
            paddedNodes.append(
                {
                    'activation': node['activation'], 
                    'group': node['group'], 
                    'id': node['id'], 
                    'shortName': node['shortName'], 
                    'grpColor': node['grpColor'],
                    "id_MRBase":node["id_MRBase"],
                    "activColor" : "white",
                    "currIntvLvl" : 0,
                    "totalFunds" : 0
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
                }
                
            )
        
        
        dummyCount_links = len(paddedLinks[0])-5
            
        #messages
        message="**:  {} game dummy properties added to nodes and {} added to links".format(dummyCount_nodes,dummyCount_links)
        return (paddedNodes, paddedLinks, message)
