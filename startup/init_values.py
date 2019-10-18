#Import
import json #converting json objects in python

def Start_Values(): #make copy of original start data
    with open("startup/playable_health_v5.json") as json_file:
        dat = json.load(json_file)
    with open("models/data.json", "w") as json_file:
        json.dump(dat, json_file, indent=4, sort_keys=True)
