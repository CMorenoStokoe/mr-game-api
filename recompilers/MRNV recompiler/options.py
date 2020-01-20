################################
#CUSTOMISATION PARAMATERS 
#(edit these values to change recompiler function)
################################

#Bonferroni correct?
bonferroniCorrect = False

#Addons enabled:
betterNames_enabled = True
#Info:
#betterNames shortens and makes more easily understandable trait names
negativeScoring_enabled = True
#Info:
#Reverses the beta of links to/from nodes which are negatively scored (i.e., higher scores actually indicate lower trait level)
safeNames_enabled = True
#Info:
#safeNames converts trait names into names safe for processing (i.e., removes / which is confused for breka characters and * which is confused for wildcards)

#Grouping mode:
grouping_mode = 'Game'
#Set groups ('Game' mode only)
policies = ['UKB-b:4424','UKB-b:8476','UKB-b:4710','UKB-b:4077','UKB-b:10162','UKB-b:5779','961','UKB-b:1585','UKB-b:4779','UKB-b:17999','1239','UKB-b:19953']
goals = ['1018','22','1187','UKB-b:6519','1189','UKB-b:5238']
#Info:
#Grouping mode sets the 'group' attribute for nodes. 'Game' groups nodes into policies and goals. 'Auto' groups nodes into groups according to their prefixes (e.g., 'ICD-10 Diagnosis: [trait] ') and a pre-defined list.
#Node IDs in the list of policies will be defined as policies, and node IDs in the list of goals will be identified as goals.
