class Model_ClG():
        
    def coloredGroups(recompiledNodes,colorScheme):
        
        #Define colorschemes
        if colorScheme == "Binary":
            colors=["green", "lightgray"]
        elif colorScheme == "Strong":
            colors=["cornflowerblue", "violet", "lightseagreen", "brown", "forestgreen", "red",  "purple", "goldenrod", "crimson", "cadetblue"]
        elif colorScheme == "Pastel":
            colors=["cornflowerblue", "lightcoral", "lightcyan", "lightgreen", "lightgray", "lightpink",  "lightsalmon", "lightgoldenrodyellow", "lightseagreen","black"]
        elif colorScheme == "grayscale":
            colors=["gray", "black", "darkgray", "dimgray", "lightgray", "slategray",  "darkslategray", "lightslategray", "beige", "lightdimgray"]
        else:
            colors=["red"]
        
        #Build list of groups in data
        groups={}
        count=0
        for node in recompiledNodes:
            if node["group"] not in groups:
                groups[node["group"]]=colors[count]
                count+=1
        
        #Color nodes by groups 
        nodes=[]
        for node in recompiledNodes:
            nodes.append(
                            {
                                "activation": node["activation"],
                                "group": node["group"],
                                "id": node["id"],
                                "shortName": node["shortName"],
                                "grpColor": groups[node["group"]],
                                "id_MRBase":node["id_MRBase"]
                            }
            )
        
        printout = "**:  Color scheme set: {}".format(colorScheme)
        return(nodes, printout)