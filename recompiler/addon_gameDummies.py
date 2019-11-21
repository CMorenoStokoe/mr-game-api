class Model_GD():
        
    def gameDummies(nodeList,linkList):
        
        #1) Add to nodes dummmy properties for game to use
        
        paddedNodes = []
        
        for node in nodeList:
            paddedNode = {
                            "id" : node['id'],
                            "shortName" : node['shortName'],
                            "group" : node['group'],
                            "grpColor": node['grpColor'],
                            "activation" : node['activation'],
                            "activColor" : "Gray",
                            "currIntvLvl" : 0,
                            "totalFunds" : 0,
                          }
            paddedNodes.append(paddedNode)
        
        #2) Add to links dummmy properties for game to use
        
        paddedLinks = []
        
        for link in linkList:
            paddedLink = {
                            "value": link['value'],
                            "color": link['color'],
                            "id": link['id'],
                            "source": link['source'],
                            "target": link['target'],
                            "currIntvLvl" : 0,
                          }
            paddedLinks.append(paddedLink)
            
            
        #messages
        message="**:  {} game dummy properties added to nodes and {} added to links".format(len(paddedNode)-5,len(paddedLink)-5)
        return (paddedNodes, paddedLinks, message)
