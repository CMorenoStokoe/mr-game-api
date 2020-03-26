class Model_CG():
        
    def collapsedGroups(nodeList,linkList,groupDict):
        collapsedNodesN=0
        collapsedLinksN=0
        counter3 = 1
        collapseGroupMembers = []

        #optional group collapse criteria
            #(edit this list to change which groups collapse)
            #(find group numbers from python console output from running main script once first)
        collapsedGroupNumbers = [
                                    2,
                                    6,
                                    8
                                ]
        #iterate over nodes to identify target group members
        nodes=[]
        links=[]
        groupNames={}
        collapsedIDs=[]
        collapsedGRPs=[]
        dictNewIDs={}
        for group,num in groupDict.items():
            groupNames[num]=group
        
        #Identify nodes to collapse and collapse them
        nodes=([i for i in nodeList if i["group"] not in collapsedGroupNumbers])
        nodesCollapsable=([i for i in nodeList if i["group"] in collapsedGroupNumbers])
        c=[]
        d=[]
        for node in nodesCollapsable:
            collapseGroupMembers.append(node["id"])
            dictNewIDs[node["id"]]="MNRV_GRP:{}".format(node['group'])
            if node["group"] not in c:#Build one new node which represents all traits in a collapsed group
                c.append(node["group"])
                d.append(
                                {
                                    "id" : "MNRV_GRP:{}".format(node['group']),
                                    "short_name" : groupNames[node['group']],
                                    "group" : node['group'],
                                }
                        )
        for node in d:
            nodes.append(node)
        
        #Identify links to collapse and collapse them
        for link in linkList:
            if link["source"] in collapseGroupMembers:
                source = dictNewIDs[link["source"]]
                collapsedLinksN+=1
            else:
                source = link['source']
            if link["target"] in collapseGroupMembers:
                target = dictNewIDs[link["target"]]
                collapsedLinksN+=1
            else:
                target = link['target']
            links.append(
                {
                    "b": link['b'],
                    "color": link['color'],
                    "id": link['id'],
                    "nsnp": link['nsnp'],
                    "pval": link['pval'],
                    "se": link['se'],
                    "source": source,
                    "target": target
                }
            )

        #Filter out multiple nodes
        filterN=[]
        dictRpNs={}
        for node in nodes:
            dictRpNs[node['id']]=0
        for node in nodes:
            dictRpNs[node['id']]+=1
            if not dictRpNs[node['id']]>=2:
                filterN.append(node)
        nodes=filterN
        #Filter out self-referencing links
        filterL = [i for i in links if i['source'] != i['target']]
        selfRefsGRP=(len(links)-len(filterL))
        links=filterL 
        
                #messages
        info_flag = 1
        collapsedGroupsN=(len(collapsedGroupNumbers))
        message1="**:  {} nodes and {} links collapsed across {} groups (see code)".format(len(nodesCollapsable),collapsedLinksN,len(collapsedGroupNumbers))
        message2=("**:  {} intra-group references identified and excluded (e.g., Exercise trait 1-->Exercise trait 2) ").format(selfRefsGRP)
        
        return(nodes,links,message1,message2)
