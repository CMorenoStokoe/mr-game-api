class Model_LC():
        
    def linkCount(recompiledEdges):
        edgeDict=[]
        edgeDict2=[]
        edgeCount=[]
        for edge in recompiledEdges:
            edgeDict.append(edge['source'])
            edgeDict.append(edge['target'])
            if edge['source'] not in edgeDict2:
                edgeDict2.append(edge['source'])
            if edge['target'] not in edgeDict2:
                 edgeDict2.append(edge['target'])
        for edge in edgeDict2:
            x = {"node":edge,"count":edgeDict.count(edge)}
            if x not in edgeCount:
                edgeCount.append(x)
        eg = sorted(edgeCount, key=lambda k: k['count'])
        printout = ["##  Count of edges:",eg]
        return(printout)