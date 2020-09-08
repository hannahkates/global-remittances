import csv
import json
import random

with open('Bilateralremittancematrix2018Oct2019.csv', newline='') as csvfile:
    mydata = list(csv.reader(csvfile))
# note: sender countries are rows. recipient countries are columns.

# function that consumes the adjacency matrix from the CSV and
# outputs the final json structure for d3 chart containing nodes and links
def convert(adj_mtx):

    # create list of countries
    countries = adj_mtx[0][1:]

    # store length of list of countries for iteration
    ctry_len = len(countries)

    # create simpler matrix without country label row and column
    adj_mtx = adj_mtx[1:ctry_len+1]

    for row in adj_mtx:
        row = row.pop(0)

    # specify minumum transfer $ amount to filter links by
    min_transfer = 1000

    # create empty list called links that will store all the filtered links
    links = []

    # skip row 0 because it contains country labels
    for i in range(ctry_len):

        # get country label from column 0
        sender = countries[i]

        # only look at columns for countries that haven't been iterated through yet
        # this avoids the creation of duplicate links
        # we also never want a case where j==i
        for j in range(i+1, ctry_len):

            # get recipient country label from row 0
            recipient = countries[j]

            # how much did the sender send to the recipient?
            sent = float(adj_mtx[i][j].replace('N/A', '0'))

            # how much did the recipient send back to the sender?
            received = float(adj_mtx[j][i].replace('N/A', '0'))

            # calculate net
            net = sent-received

            # exclude links where neither country sent money
            if(abs(net) > 0):

                # if sender sent more than they received back (positive net)
                if(net > min_transfer):
                    links.extend( [{
                        "source":sender,
                        "target":recipient,
                        "value":net,
                        "sourceToTarget":sent,
                        "targetToSource":received
                    }] )

                # if sender recevied more than they sent (negative net)
                elif(abs(net) > min_transfer):
                    links.extend( [{
                        "source":recipient,
                        "target":sender,
                        "value":-1*net,
                        "sourceToTarget":received,
                        "targetToSource":sent
                    }] )

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
        nodes.extend( [{
            "index":i,
            "name":used_nodes[i],
            "color":"#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        }] )
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

with open('data.json', 'w') as outfile:
    json.dump(convert(mydata), outfile)
