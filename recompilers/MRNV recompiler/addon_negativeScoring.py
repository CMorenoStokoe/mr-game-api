import json

with open('addon_negativeScoring_CMS.json') as json_file:
        negativeScoringTable = json.load(json_file)

class Model_NS():
        
    def negativeScoring(nodeList,linkList):
        negativelyScoredIDs=[]
        correctedLinks=0
        ignoredLinks=0
        normalLinks=0
        
        for node in nodeList:
            if node["id"] in negativeScoringTable:
                negativelyScoredIDs.append(node["id"])
        
        for link in linkList:
            nsVAL=0
            if (link["source"] in negativelyScoredIDs):
                nsVAL +=1
            if (link["target"] in negativelyScoredIDs):
                nsVAL +=1
            if nsVAL == 1:
                if link["color"]=="blue":
                    link["color"]="red"
                elif link["color"]=="red":
                    link["color"]="blue"
                link["b"]=link["b"]*-1
                correctedLinks+=1
            elif nsVAL == 2:
                ignoredLinks+=1
            else:
                normalLinks+=1

        #messages
        negativelyScored=(len(negativelyScoredIDs))
        message="**:  {} negatively scored traits identified ({} corrected, {} double-negatives)".format(negativelyScored,correctedLinks,ignoredLinks)
        
        return(nodeList,linkList,message)
