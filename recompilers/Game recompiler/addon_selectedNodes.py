import random

class Model_SN():
        
    def selectedNodes(nodeList,linkList,params):
        nodes=[]
        nodeIDs=[]
        links=[]
        
        if params[0] == "ALL":
            nodes=nodeList
            links=linkList
            
        elif params[0] == "N_RANDOM":
            random.shuffle(nodeList)
            nodes = nodeList[0:params[1]]
            nodeIDs = [i["id"] for i in nodes]
            print(nodes)
            links0 = [i for i in linkList if i["source"] in nodeIDs]
            links1 = [i for i in links0 if i["target"] in nodeIDs]
            for link in links1:
                if link not in links:
                    links.append(link)
                    
        elif params[0] == "N_NAMED":
            nodes = [i for i in nodeList if i["id"] in params[1]]
            links0 = [i for i in linkList if i["source"] in params[1] and i["target"] in params[1]]
            for link in links0:
                if link not in links:
                    links.append(link)
                    
        elif params[0] == "N_RELATED": 
            nodes0=[]
            links0=[]
            relatedParams=[]
            for param in params[1]:
                nodes0=[i["id"] for i in nodeList if i["id"] in params[1]]
            for i in linkList:
                if i["source"] in params[1]:
                    if i["target"] not in nodes0:
                        nodes0.append(i["target"])
                        relatedParams.append(i["target"])
                    if i["target"] not in links0:
                        links0.append(i)
                if i["target"] in params[1]:
                    if i["source"] not in nodes0:
                        nodes0.append(i["source"])
                        relatedParams.append(i["source"])
                    if i["source"] not in links0:
                        links0.append(i)
            for i in linkList:
                if i["source"] in relatedParams:
                    if i["target"] in relatedParams:
                        links0.append(i)  
            links=links0
            for node in nodeList:
                if node["id"] in nodes0:
                    nodes.append(node)
                    
        message="**:  {}/{} nodes and {}/{} links selected with paramaters: {}".format(len(nodes),len(nodeList),len(links),len(linkList),params)
        return(nodes,links,message)
