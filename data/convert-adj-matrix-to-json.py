import csv
import json

with open('Bilateralremittancematrix2018Oct2019.csv', newline='') as csvfile:
    mydata = list(csv.reader(csvfile))

def convert(adjacency_list):
    # skip the index of 0, because in the CSV, row 0 and column 0 are used for the country names

    # create empty list called links that will be populated during the for loop
    links = []

    # specify minumum transfer $ amount to filter links by
    min_transfer = 2500

    for i,adj in enumerate(adjacency_list):
        # skip row 0 since it contains country names, not data
        if(i > 0):
            # iterate through each item in the row, skipping column 0
            for n in range(1, len(adj)):
                # two conditions for recording links:
                # - avoid circular reference. a country shouldn't send remittances to itself
                # - only keep links where remittances > 0
                if (i != n) & (adj[n] != 'N/A'):
                    if float(adj[n]) > min_transfer:
                        # store the source and target indices, renumbering with index 1 as 0
                        links.extend( [{"source":adj[0],"target":mydata[0][n],"value":float(adj[n])}] )

    used_nodes = []
    for i in links:
        used_nodes.append(i["source"])
        used_nodes.append(i["target"])

    used_nodes = sorted(list(set(used_nodes)))

    nodes = []
    for i in range(len(used_nodes)):
        nodes.extend( [{"index":i, "name":used_nodes[i]}] )
        for l in links:
            if (l["source"] == used_nodes[i]):
                l["source"] = i
            if (l["target"] == used_nodes[i]):
                l["target"] = i

    return {"nodes":nodes, "links":links}

convert(mydata)

with open('data.json', 'w') as outfile:
    json.dump(convert(mydata), outfile)
