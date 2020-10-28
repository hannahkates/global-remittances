# Data Viz: Global Flow of Remittances

## About
This is a simple vanilla JavaScript application with a d3.js sankey data visualization. The chart displays the flow of remittances between all countries in the world over $3 billion. It shows the transfer relationships and estimated amounts. The repo also includes all the python script used prepare the data.

## Data source
[World Bank, Bilateral Remittance Matrix 2018 (updated October 2019)](https://www.worldbank.org/en/topic/labormarkets/brief/migration-and-remittances)

## Data preparation
The data published by the World Bank is stored in an excel spreadsheet in an adjacency matrix format. The d3 network chart must consume a JSON file formatted to a specific standard, listing all the "nodes" and then the "links". [Explanation of necessary JSON data structure](https://www.d3-graph-gallery.com/graph/network_data_format.html).

**Data munging steps:**
- Download excel spreadsheet from World Bank website and open in excel.
- Remove extra columns and rows leaving only the matrix of individual countries, making sure to exclude the grand total column and grand total row.
- Save as a CSV file. See [Bilateralremittancematrix2018Oct2019.csv](https://github.com/hannahkates/global-remittances/blob/master/data/Bilateralremittancematrix2018Oct2019.csv)
- Run [convert-adj-matrix-to-json.py](https://github.com/hannahkates/global-remittances/blob/master/data/convert-adj-matrix-to-json.py) python script to reformat the adjacency matrix CSV into the required JSON format.
  - :warning: NOTE: This python script also filters which records to include based on the size of the transfer. The minimum is currently set to $3000 million, yielding ~30 country nodes. The app timed out when more nodes were included.
- App uses [data.json](https://github.com/hannahkates/global-remittances/blob/master/data/data.json) outputted by the python script.

## Dependencies
- d3 v4
- d3 sankey. I copied the [sankey code](https://github.com/d3/d3-plugins/tree/master/sankey) directly [into this repo](https://github.com/hannahkates/global-remittances/blob/master/js/sankey.js) because I had trouble finding a stable, secure link to a hosted version online.
- To implement tooltips, I used d3-tip.js written by Justin Palmer. I [copied the code directly into this repo](https://github.com/hannahkates/nyc-water/blob/master/js/d3-tip.js) because I had trouble finding a stable, secure link to a hosted version online.

## How to run this application locally
- Clone repo `git clone https://github.com/hannahkates/global-remittances.git`
- Run using python dev server `python -m SimpleHTTPServer` (or other local server options like Atom Live Server)

## Resources
This build was guided by these blog posts:
- https://bl.ocks.org/d3noob/013054e8d7807dff76247b81b0e29030
- https://bl.ocks.org/micahstubbs/3c0cb0c0de021e0d9653032784c035e9
