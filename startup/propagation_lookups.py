import json
#Build dictionaries for quickly looking up values for propagation
def Scout():
    linkedNodes={}
    link_values={}
    with open('playable_health_v5.json') as json_file:
        dat = json.load(json_file)
        #Build dictionary of linked nodes
        for link in dat["links"]:
            if link["source"] in linkedNodes:
                linkedNodes[link["source"]].append(link["target"])
            elif:
                linkedNodes[link["source"]] = [link["target"]]
        #Build dictionary of link effects
        for node in linkedNodes:
            for link in dat["links"]:
                
        link_values[link["source"]]={link["target"]:link["value"]}
    print(linkedNodes,link_values)
    if "Gout" in linkedNodes:
        for link in link_values:
            print(link_values[link])
Scout()