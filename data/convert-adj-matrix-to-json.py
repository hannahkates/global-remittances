import csv
import json

with open('Bilateralremittancematrix2018Oct2019.csv', newline='') as csvfile:
    mydata = list(csv.reader(csvfile))

def convert(adjacency_list):
    # skip the index of 0, because in the CSV, row 0 and column 0 are used for the country names

    # create list of nodes, including their index (renumbering with index 1 as 0) and name
    nodes = [{"index": i-1, "name": mydata[0][i]} for i in range(1, len(adjacency_list))]

    # create empty list called links that will be populated during the for loop
    links = []

    for i,adj in enumerate(adjacency_list):
        # skip row 0 since it contains country names, not data
        if(i == 2):
            # iterate through each item in the row, skipping column 0
            for n in range(1, len(adj)):
                # store the source and target indices, renumbering with index 1 as 0
                links.extend( [{'source':i-1,'target':n-1,'value':adj[n]}] )

    return {"nodes":nodes, "links":links}

convert(mydata)

with open('data.json', 'w') as outfile:
    json.dump(convert(mydata), outfile)
