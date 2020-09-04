import csv
import json

with open('Bilateralremittancematrix2018Oct2019.csv', newline='') as csvfile:
    mydata = list(csv.reader(csvfile))

# function that consumes the adjacency matrix from the CSV and
# outputs the final json structure for d3 chart containing nodes and links
def convert(adjacency_list):

    # specify minumum transfer $ amount to filter links by
    min_transfer = 3000

    # create empty list called links that will store all the filtered links
    links = []

    # identify all links that have values over the minimum transfer $ amount
    for i,adj in enumerate(adjacency_list):
        # skip row 0 since it contains country names, not data
        if(i > 0):
            # iterate through each item in the row, skipping column because it contains the country name
            for n in range(1, len(adj)):
                # three conditions for recording links:
                # - avoid circular reference. a country shouldn't send remittances to itself
                # - skips links where value is "N/A"
                # - filter for links where value is more than minumum transfer $ amount
                if (i != n) & (adj[n] != 'N/A'):
                    if float(adj[n]) > min_transfer:
                        # store the source and target country names and tranfer value
                        links.extend( [{"source":adj[0],"target":mydata[0][n],"value":float(adj[n])}] )

    # create an empty array for storing all the nodes present in the filtered links
    used_nodes = []

    # append all the source and target nodes into the used_nodes list
    for i in links:
        used_nodes.append(i["source"])
        used_nodes.append(i["target"])

    # create sorted list of unique nodes
    used_nodes = sorted(list(set(used_nodes)))

    # create an empty list for storing the nodes for the final json object
    nodes = []

    # for loop prepares nodes and links for the final json object
    # nodes: it stores the node index in addition to the name
    # link: it updates the links object by replacing the node country names with indices
    for i in range(len(used_nodes)):
        nodes.extend( [{"index":i, "name":used_nodes[i]}] )
        for l in links:
            # if source country name == country name
            if (l["source"] == used_nodes[i]):
                # overwrite country name with county's node index
                l["source"] = i
            # if target country name == country name
            if (l["target"] == used_nodes[i]):
                # overwrite country name with county's node index
                l["target"] = i

    # final json structure for d3 chart
    return {"nodes":nodes, "links":links}

convert(mydata)

with open('data.json', 'w') as outfile:
    json.dump(convert(mydata), outfile)
