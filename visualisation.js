chart = {
  const links = data.links.map(d => Object.create(d));
  const nodes = data.nodes.map(d => Object.create(d));

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX())
      .force("y", d3.forceY());

  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

  const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .join("line")
        .attr("stroke-width", 1)
        .attr("stroke", d => d.color)//edge color as function of beta weight sign//
        .attr("stroke-opacity", d => Math.abs(d.value)/20)//edge opacity as function of beta weight value//
      .attr("marker-end", "url(#end)");

  const node = svg.append("g")
    .selectAll(".node")
    .data(nodes)
    .join("g")
      .attr('class', 'node')
      .call(drag(simulation));

 // From https://stackoverflow.com/questions/28050434/introducing-arrowdirected-in-force-directed-graph-d3
  svg.append("svg:defs").selectAll("marker")//edge color as function of beta weight sign//
      .data(["end"])      // Different link/path types can be defined here 
    .enter().append("svg:marker")    // This section adds in the arrows
      .attr("id", String)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", -1.5)
      .attr("markerWidth", 5)
      .attr("markerHeight", 5)
      .attr("stroke", "#999")
      .attr("fill", "#999")
      .attr("orient", "auto")
    .append("svg:path")
      .attr("d", "M0,-5L10,0L0,5")

  node.append('circle')
      .attr("r", d => d.activation*5)
      .attr("fill", color);
  
  node.append("text")
      .text(function(d) {
        return d.id;
      })
      .style('fill', '#000')
      .style('font-size', '12px')
      .attr('x', 6)
      .attr('y', 3);

  simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("transform", d => `translate(${d.x}, ${d.y})`)
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
  });

  invalidation.then(() => simulation.stop());

  return svg.node();
}


data = d3.json("https://gist.githubusercontent.com/CMorenoStokoe/066933f94519f022028c20bda562f09c/raw/6348afab1ee698eac7407049a692cdeeb38efc41/playable_health_v5.json") //Create object in memory for edit


height = 600


color = {
  const scale = d3.scaleOrdinal(d3.schemeCategory10);
  return d => scale(d.group);
}


drag = simulation => {
  
  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  
  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }
  
  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
  
  return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}


d3 = require("d3@5")