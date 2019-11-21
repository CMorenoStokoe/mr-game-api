################################
#CUSTOMISATION PARAMATERS 
#(edit these values to change recompiler function)
################################

#Default node activation value:
default_node_activation = 10 
#Info:
#Change this value to specify the default activation value for nodes in the data

#Number of nodes:
number_of_nodes = None 
#Info:
#Change 'none' to number to specify the number of nodes extracted from the data

#Excluded nodes
excluded_nodes = ["Father's age at death"] 
#Info:
#Change 'none' to a [list,] of IDs of nodes to ignore it and its links 

#Collapse all groups
collapse_all_groups = False 
#Info:
#Change to 'True' to collapse all nodes within the same group into one node

#Count links per node
count_links_per_node = False 
#Info:
#Change to 'True' to print in console the number of links each node has

#Color scheme
colorScheme = "Strong"
#Change value to set colour scheme. Choices: Strong (strongly colored), Pastel (lightly colored) and Greyscale (largely non-colored)

#Selected nodes
selected_nodes = ['N_NAMED',['Body mass index','Height','Well-being','Intracranial volume','Years of schooling', 'Red blood cell count', 'Total cholesterol', 'Fasting insulin', 'Cigarettes smoked per day', 'Coronary heart disease', 'Extreme height', 'Platelet count', 'Iron', 'Lung cancer','Urate','HbA1C','Birth weight','Mean cell volume','Conscientiousness','Lung cancer','Schizophrenia','Sleep duration',"Alzheimer's disease","Liver Disease(PBC)",'Zinc']]
#Info:
#Change to select nodes.
#(1)For first item in list, options are: 'ALL' (select all nodes), 'N_RANDOM' (select x nodes at random), 'N_NAMED' (select x nodes by ID), 'N_RELATED' (selects node(s) and all related).
#For second item in list, options correspond to choice above ^. For 'ALL', pass None. For 'N_RANDOM' pass a number to set the number of nodes randomly selected (e.g., 7 will pull 7 nodes from the network at random). For 'N_NAMED', pass a list of IDs for nodes to pull (e.g., 'Gout' will only pull the node with the ID 'Gout'). For 'N_RELATED' pass a list of IDs for node(s) and neighbour(s) to pull.
#for example, for named nodes: 
example = ['N_NAMED',['Body mass index','Height','Well-being','Intracranial volume','Years of schooling', 'Red blood cell count', 'Total cholesterol', 'Fasting insulin', 'Cigarettes smoked per day', 'Coronary heart disease', 'Extreme height', 'Platelet count', 'Iron', 'Lung cancer','Urate','HbA1C','Birth weight','Mean cell volume','Conscientiousness','Lung cancer','Schizophrenia','Sleep duration',"Alzheimer's disease","Liver Disease(PBC)",'Zinc']]
################################