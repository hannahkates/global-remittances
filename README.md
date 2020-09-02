# Data Viz: Global Network of Remittances

## About
This is a d3.js data visualization of remittances between all countries in the world. It shows the transfer relationships and estimated amounts.

## Data source
World Bank, Bilateral Remittance Matrix 2018 (updated October 2019)
https://www.worldbank.org/en/topic/labormarkets/brief/migration-and-remittances

## Data preparation
The data published by the World Bank is stored in an excel spreadsheet in an adjacency matrix format. The d3 network chart must consume a JSON file formatted to a specific standard, listing all the "nodes" and then the "links".

#### Explanation of necessary JSON data structure:
https://www.d3-graph-gallery.com/graph/network_data_format.html

#### Data munging steps:
- Download excel spreadsheet and open in excel.
- Remove extra columns and rows leaving only the matrix of individual countries.
- Save as a CSV file. See Bilateralremittancematrix2018Oct2019.csv
- Run python script to reformat the adjacency matrix CSV into a JSON format.

## How to run this application
