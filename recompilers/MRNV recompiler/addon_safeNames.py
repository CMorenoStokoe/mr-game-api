#debug options
debug_MRNV_addon_safeNames = False

class Model_SafN():
        
    def safeNames(recompiledNodes):
        safeNodes=[]
        safeEdges=[]
        
        safeNodeCount=0
        safeEdgeCount=0
        infringements_total=0
        
        #Name en-safener function
        def ensafen(name):
            infringementCount=0
            name_safe = name
            if '*' in name:
                infringementCount+=1
                name_safe = name_safe.replace('*',' ')
                if debug_MRNV_addon_safeNames == True:                     print("debug_MRNV_addon_safeNames: name infringement found: {}. Corrected to: {}".format(name,name_safe))
            if ' / ' in name:
                infringementCount+=1
                name_safe = name_safe.replace('/','or')
                if debug_MRNV_addon_safeNames == True:                     print("debug_MRNV_addon_safeNames: name infringement found: {}. Corrected to: {}".format(name,name_safe))
            if '/' in name:
                infringementCount+=1
                name_safe = name_safe.replace('/',' per ')
                if debug_MRNV_addon_safeNames == True:                     print("debug_MRNV_addon_safeNames: name infringement found: {}. Corrected to: {}".format(name,name_safe))
            if '\\' in name:
                infringementCount+=1
                name_safe = name_safe.replace('\\',' ')
                if debug_MRNV_addon_safeNames == True:                     print("debug_MRNV_addon_safeNames: name infringement found: {}. Corrected to: {}".format(name,name_safe))
            return (name_safe,infringementCount)
        
        #Remove potentially unsafe characters from IDs
        for node in recompiledNodes:
            safe_output = ensafen(node["name"])
            name = safe_output[0]
            infringements = safe_output[1]
            
            #Append safe names to updated node list
            safeNodes.append({
                "group": node["group"],
                "id": node["id"],
                "name": name,
                "short_name": node["short_name"]
            })
            
            #Track number of changes
            if infringements >= 1: 
                safeNodeCount+=1 
                infringements_total+=infringements
        
        
        message = "**:  {} name infringements across {} nodes identified and corrected to safe formatting".format(infringements_total,safeNodeCount)
        
        return(safeNodes, message)