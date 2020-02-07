class Model_EC():
    def __init__(self):
        self.nodes=[]
        self.links=[]

    def exclusionCriteria(nodeList,linkList,excl):
        nodesn=(len(nodeList))
        linksn=(len(linkList))
        #optional exclusion criteria
            #(edit this list to change excluded IDs)
        excludedTraitIDs = excl
            #filters for nodes and links
        filterN = [i for i in nodeList if i['id'] not in excludedTraitIDs]
        nodeList = filterN
        filterL = [i for i in linkList if i['source'] not in excludedTraitIDs and i['target'] not in excludedTraitIDs]
        linkList = filterL
        
            #messages
        excludedN = nodesn-len(nodeList)
        excludedL = linksn-len(linkList)
        info_flag = 1
        message="**:  {} nodes and {} links removed due to exclusion criteria (see code)".format(excludedN,excludedL)
        
        return (nodeList, linkList, message)
      