import json
import os.path
from decimal import *

#setup_warnings(ignore)
warn_format1=None
flag_format1=0
warn_format2=None
flag_format2=1
warn_format3=None
flag_format3=1
info_flag=0
info_optional=None
flag_noName=0
err_noName=None
groupMessage=None

#debug options
debug_MRNV = False
 
#open files for transformation
with open('MRNV_input.json') as json_file:
    data = json.load(json_file)
    
from options import *

if betterNames_enabled == True:
    ao_betterNames = os.path.exists("addon_betterNames_CMS.json")
    if (ao_betterNames==True):
        from addon_betterNames import betterNames
if negativeScoring_enabled == True:
    ao_negativeScoring = os.path.exists("addon_negativeScoring.py")
    if (ao_negativeScoring==True):
        from addon_negativeScoring import Model_NS
if safeNames_enabled == True:
    ao_safeNames = os.path.exists("addon_safeNames.py")
    if (ao_safeNames==True):
        from addon_safeNames import Model_SafN
#support for legacy addons:
ao_exclusionCriteria = os.path.exists("addon_exclusionCriteria.py")
if (ao_exclusionCriteria==True):
    from addon_exclusionCriteria import Model_EC
ao_collapsedGroups = os.path.exists("addon_collapsedGroups.py")
if (ao_collapsedGroups==True):
    from addon_collapsedGroups import Model_CG


#initialise variables for dictionary lists, data linkss and counter for automatically incrementing ID#s
print("***Start***")#delinieates start of print out in console because printout is messy
dictID = {}
dictGRP = {}
dictGRPmembers = {}
dictNMID={}
links = []
nodes_list = []
nodes_listNm = []
nodes = []
links_corrected = []
counter = 1
counter2 = 1
selfRefs = 0
print("*10% Done: JSON found and startup completed")

#Compile dictionary of IDs : trait names mappings & IDs : group mappings e.g., exercise measures
for row in data:
    #selects only Wald/IVW estimates & valid tests (i.e., where beta=/=1.0)
    
    if (row["method"]=="Wald ratio") or (row["method"]=="Inverse variance weighted"):
        if (row["outcome"]==row["exposure"]):
            selfRefs+=1
        if not (row["outcome"]==row["exposure"]):
            
            #selects rows with MR base name||id format, and shortens their names
            if (' || ' in row["outcome"] and ' || ' in row["exposure"]):
                out_name=row["outcome"].split(' || ')[0]
                exp_name=row["exposure"].split(' || ')[0]
                
                #PLACEHOLDER CODE FOR EXTRACTING IDs
                #out_id=row["outcome"].split(' || ')[1]
                #exp_id=row["exposure"].split(' || ')[1]
                
                #Identifying groups of traits in data, and populating group dictionary
                
                    #Search 1) For groups indicated in name by colon(:), AND shortening their names 
                    
                if (': ' in row["exposure"]):
                    dictGRPmembers[row["id.exposure"]]=exp_name.split(': ')[0]
                    if row["exposure"].split(': ')[0] not in dictGRP:
                        dictGRP[exp_name.split(': ')[0]]=counter
                        dictGRPmembers[row["id.exposure"]]=counter
                        counter+=1
                    exp_name = exp_name.split(': ')[1]
                    flag_format2 = 0
                if (': ' in row["outcome"]):
                    dictGRPmembers[row["id.outcome"]]=out_name.split(': ')[0]
                    if row["outcome"].split(': ')[0] not in dictGRP:
                        dictGRP[out_name.split(': ')[0]]=counter
                        counter+=1
                    out_name = out_name.split(': ')[1]
                    flag_format2 = 0
                    
                    #Search 2) For groups indicated in name by specific phrase (e.g., for activity)
                    
                if ('activity' in row["exposure"]):
                    dictGRPmembers[row["id.exposure"]]="Exercise"
                    if "Exercise" not in dictGRP:
                        dictGRP["Exercise"]=counter
                        counter+=1
                    flag_format3 = 0
                if ('activity' in row["outcome"]):
                    dictGRPmembers[row["id.outcome"]]="Exercise"
                    if "Exercise" not in dictGRP:
                        dictGRP["Exercise"]=counter
                        counter+=1
                    flag_format3 = 0

            #Populating dictionary of id:name mappings
                dictID[row["id.outcome"]]=out_name
                dictID[row["id.exposure"]]=exp_name
                dictNMID[out_name]=[row["id.outcome"]]
                dictNMID[exp_name]=[row["id.exposure"]]

            #Populating list of unique traits in data, for nodes list
                if (row["id.outcome"] not in nodes_list): 
                    nodes_list.append(row["id.outcome"])
                if (row["id.exposure"] not in nodes_list): 
                    nodes_list.append(row["id.exposure"])
                if (row["outcome"] not in nodes_listNm): 
                    nodes_listNm.append(dictID[row["id.outcome"]])
                if (row["exposure"] not in nodes_listNm): 
                    nodes_listNm.append(dictID[row["id.exposure"]])
            
            #Populating list of links 
                row["nsnp"] = int(row["nsnp"])
                row["b"] = round(float(row["b"]),2)
                row["se"] = round(float(row["se"]),2)
                row["pval"] = float(row["pval"])
                if (row["b"]<=0):
                    color = "blue"
                elif (row["b"]>=0):
                    color = "red"
                links.append(
                        {
                            "id":counter2,
                            "target":row["id.outcome"],
                            "source":row["id.exposure"],
                            "nsnp":row["nsnp"],
                            "b":row["b"],
                            "se":row["se"],
                            "pval":row["pval"],
                            "color":color
                        }
                )
                counter2+=1
       
            else:
                flag_format1 = 1   

print("*30% Done: Links produced")
print("**: ", len(links), " IVW/Wald links identified from ", len(data), " rows of JSON data.")
print("**: ", selfRefs, " self-references identified and ignored (e.g., BMI-->BMI) ")


#Produce nodes 
if grouping_mode == 'Auto':
    
        #Import auto-identified groups
    dictGRPmembersFinal = {}
    dictIDFinal = {}
    for node in nodes_list:
        if node in dictGRPmembers:
            dictGRPmembersFinal[node]= dictGRPmembers[node]
            
        #Import additional groups and names from addon (if available)
    if (ao_betterNames == True):
        BN=betterNames(dictGRP,dictGRPmembersFinal,dictIDFinal,counter,nodes_list,nodes_listNm,dictNMID)
        dictGRP=BN[0]
        dictGRPmembersFinal=BN[1]
        dictIDFInal=BN[2]

        #Constructing node list from group and shortName dictionaries
    for node in nodes_list:
        name=None
        if node in list(dictIDFinal.keys()):
            name = dictIDFinal[node]
        else:
            name = dictID[node]
        if node in list(dictGRPmembersFinal.keys()):
            group9 = dictGRPmembersFinal[node]
            group=dictGRP[group9]
        else:
            group = 0
        nodes.append(
            {
                "id" : node,
                "short_name" : name,
                "group" : group
            }
        )
        
    print("**: {} groups identified in data: {}".format(len(dictGRP),dictGRP))


elif grouping_mode == 'Game':
    #Import betterNames list
    from addon_betterNames import betterNamesTable
    
    #Import auto-identified groups
    dictGRPmembersFinal = {}
    dictIDFinal = {}
    for node in nodes_list:
        if node in dictGRPmembers:
            dictGRPmembersFinal[node]= dictGRPmembers[node]
            
    #Import additional groups and names from addon (if available)
    if (ao_betterNames == True):
        BN=betterNames(dictGRP,dictGRPmembersFinal,dictIDFinal,counter,nodes_list,nodes_listNm,dictNMID)
        dictGRP=BN[0]
        dictGRPmembersFinal=BN[1]
        dictIDFInal=BN[2]

    #Constructing node list from group and shortName dictionaries
    for node in nodes_list:
        
        #Assigning shortname
        name=dictID[node]
        short_name=dictID[node]
        for storedNode in betterNamesTable:
            if node == storedNode['id']:
                if storedNode['short_name'] != None:
                    short_name = storedNode['short_name']
    
        #Assigning policy/goal group
        counter_policies = 0
        counter_goals = 0
        
        group=None
        if node in policies:
            group = 'policy'
            counter_policies += 1
        elif node in goals:
            group = 'goal'
            counter_goals += 1
            
        nodes.append(
            {
                "id" : node,
                'name' : name,
                "short_name" : short_name,
                "group" : group
            }
        )
        
    print("**:  {} policies and {}  goals identified in data".format(counter_policies, counter_goals))
    
for node in nodes:
    if node["id"]==None:
        flag_noName=1
        noNameErrNodes+=node["id"]

print("*60% Done: Nodes produced")

#Exclusion criteria [if addon available]
if ao_exclusionCriteria == True:
    EC=Model_EC.exclusionCriteria(nodes,links)
    nodes=EC[0]
    links=EC[1]
    print(EC[2])

#Keep only significant effects at Bonferroni corrected value
if bonferroniCorrect == True:
    pval_BC = 0.05/len(links)
    for link in links:
        if (link["pval"]<=pval_BC):
            links_corrected.append(link)
    print("*90% Done: Links bonferroni corrected")
    print("**: ", len(links_corrected), " out of ", len(links), " links passed the threshold (",pval_BC,") and were kept.")
else:
    links_corrected = links

#Negative scoring [if addon available]
if ao_negativeScoring == True:
    NS=Model_NS.negativeScoring(nodes,links_corrected)
    nodes=NS[0]
    links_corrected=NS[1]
    print(NS[2])

#Collapse groups [if addon available]
if ao_collapsedGroups == True:
    AO=Model_CG.collapsedGroups(nodes,links_corrected,dictGRP)
    nodes=AO[0]
    links_corrected=AO[1]
    print(AO[2])
    print(AO[3])

#Safenames [if addon available]
#Info: Ensure names are safe for future py/js/API calls
if (ao_safeNames==True):
    #call addon method
    SafN = Model_SafN.safeNames(nodes)   
    #debug
    if debug_MRNV == True:
        print("debug_MRNV: Called safeNames method with payload: nodes: {}".format(nodes))
        print("debug_MRNV: Output from safeNames method: nodes: {}".format(SafN[0]))
    
    #update node and link lists with method output
    nodes=SafN[0]
    print(SafN[1])

print("**:  {} nodes and {} links remain".format(len(nodes),len(links_corrected)))

#Comining nodes and links, writing to JSON
combined = {"nodes":nodes,"links":links_corrected}

with open('../Game recompiler/MRNV_output.json', 'w') as json_file:
   json.dump(combined, json_file, indent=4, sort_keys=True)
print("*100% Done: Nodes & links combined, JSON written")

#setup_warningMessages(ignore)
if flag_format1 == 1:
    warn_format1 = "[WARN] WARNING: '||' not detected in some trait names. SOME DATA ROWS SKIPPED, CHECK DATA OUTPUT. Is data formatted correctly? Headers will trigger this warning appropriately"
if flag_format2 == 1:
    warn_format2 = "[WARN] WARNING: ': ' not detected in trait names. IF USING GROUPED TRAITS: is data formatted correctly with category name seperated with a colon(:) e.g., 'Physical Exercise: Hours per day' & 'Physical Exercise: Hours per week' "
if flag_format3 == 1:
    warn_format3 = "[WARN] WARNING: 'activity' not detected in trait names. IF USING GROUPED TRAITS relating to PHYSICAL ACTIVITY: is data formatted correctly where 'activity' appears in the name of all traits? e.g., 'Physical activity per day' & 'Hours per week of activity"
if info_flag ==1 :
    info_optional == "[INFO] INFORMATION: Optional exclusion criteria applied to node list, see code for criteria and comment out if not desired."
if flag_noName==1:
    err_noName == "[ERR] ERROR: Some nodes were assigned no names, internal error- something went wrong. Consult code. Nodes affected:{}".format(noNameErrNodes)
warnings = [warn_format1,warn_format2,warn_format3,info_optional,err_noName]   
for warning in warnings:
    if warning != None:
        print(warning)

print("***End***")