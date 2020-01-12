import json

with open('addon_betterNames_CMS.json') as json_file:
        betterNamesTable = json.load(json_file)
        
def betterNames(groupDict,groupMembersDict,nameDict,count,nodeIDList,nodeNamesList,nameToIDDict):
    BN_Names = {}#trait ID : better name
    BN_Groups = {}#trait ID : group name
    
    #Cross reference lists
    for record in betterNamesTable:
        if not record["id"] == None:
            if record["id"] in nodeIDList:
                #Populate list of better names
                if not record["short_name"] == None:
                    #BN_Names[record["name"]]=record["short_name"]
                    BN_Names[record["id"]]=record["short_name"]
                #Populate list of better groups
                if not record["group"] == None:
                    #BN_Groups[record["name"]]=record["group"]
                    BN_Groups[record["id"]]=record["group"]
        
    #Populate list of nodes
    for node in nodeIDList:
         if node in BN_Groups:
            groupMembersDict[node]=BN_Groups[node]
            if BN_Groups[node] not in groupDict:
                groupDict[BN_Groups[node]]=count
                count+=1
                
    #Populate list of Groups
    for node in nodeIDList:
         if node in BN_Names:
            nameDict[node]=BN_Names[node]
                
    return (groupDict, groupMembersDict, nameDict)