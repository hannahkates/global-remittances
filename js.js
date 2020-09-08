var units = "Billion USD";

// set the dimensions and margins of the graph
var margin = {top: 10, right: 10, bottom: 10, left: 0},
    width = getWidth() - margin.left - margin.right,
    height = 900 - margin.top - margin.bottom;

// format variables
var formatNumber = d3.format(",.2f"),    // zero decimal places
    format = function(d) { return formatNumber(d/1000) + " " + units; },
    color = d3.scaleOrdinal(d3.schemeCategory20);

// append the svg object to the body of the page
var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Set the sankey diagram properties
var sankey = d3.sankey()
    .nodeWidth(15)
    .nodePadding(15)
    .size([width, height]);

var path = sankey.link();

function getWidth() {
  return document.getElementById("chart").offsetWidth;
}

// load the data
d3.json("data/data.json", function(error, graph) {

  sankey
      .nodes(graph.nodes)
      .links(graph.links)
      .layout(12);

// add in the links
  var link = svg.append("g").selectAll(".link")
      .data(graph.links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", path)
      .style("stroke-width", function(d) { return Math.max(1, d.dy); })
      .sort(function(a, b) { return b.dy - a.dy; });

  // add gradient to links
  link.style('stroke', (d, i) => {
    console.log('d from gradient stroke func', d);

    // make unique gradient ids
    const gradientID = `gradient${i}`;

    const startColor = d.source.color;
    const stopColor = d.target.color;

    console.log('startColor', startColor);
    console.log('stopColor', stopColor);

    const linearGradient = svg.append('linearGradient')
        .attr('id', gradientID);

    linearGradient.selectAll('stop')
      .data([
          {offset: '10%', color: startColor },
          {offset: '90%', color: stopColor }
        ])
      .enter().append('stop')
      .attr('offset', d => {
        console.log('d.offset', d.offset);
        return d.offset;
      })
      .attr('stop-color', d => {
        console.log('d.color', d.color);
        return d.color;
      });

    return `url(#${gradientID})`;
  })

// add the link titles
  link.append("title")
        .text(function(d) {
    		return d.source.name + " → " + d.target.name + ":\n~ " +
          format(d.sourceToTarget) + "\n\n" +
          d.target.name + " → " + d.source.name + ":\n~ " +
          format(d.targetToSource) + "\n\n" +
          "Net:\n~ " +
          format(d.value);
        });

// add in the nodes
  var node = svg.append("g").selectAll(".node")
      .data(graph.nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) {
		  return "translate(" + d.x + "," + d.y + ")"; })
      .call(d3.drag()
        .subject(function(d) {
          return d;
        })
        .on("start", function() {
          this.parentNode.appendChild(this);
        })
        .on("drag", dragmove));

// add the rectangles for the nodes
  node.append("rect")
      .attr("height", function(d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      // .style("fill", "blue")
      .style('fill', function(d) { return d.color; })
      .style("stroke", "black")
    .append("title")
      .text(function(d) {
		  return d.name + "\n" + format(d.value); });

// add in the title for the nodes
  node.append("text")
      .attr("x", -6)
      .attr("y", function(d) { return d.dy / 2; })
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function(d) { return d.name; })
    .filter(function(d) { return d.x < width / 2; })
      .attr("x", 6 + sankey.nodeWidth())
      .attr("text-anchor", "start");

// the function for moving the nodes
  function dragmove(d) {
    d3.select(this)
      .attr("transform",
            "translate("
               + d.x + ","
               + (d.y = Math.max(
                  0, Math.min(height - d.dy, d3.event.y))
                 ) + ")");
    sankey.relayout();
    link.attr("d", path);
  }
});
