function visualise (spell) {
    
    const svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");
    
    let dataPromise = d3.json("http://127.0.0.1:5000/simulation")

    dataPromise.then(function draw(data) {

    const color = d3.scaleOrdinal(d3.schemeCategory10);
    const links = data.links.map(d => Object.create(d));
    const nodes = data.nodes.map(d => Object.create(d));

// Set up simulation
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    const link = svg.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", 1)
      .attr("stroke", d => d.color)//edge color as function of beta weight sign//
      .attr("stroke-opacity", d => Math.abs(d.value)/5)//edge opacity as function of beta weight value//
      .attr("marker-end", "url(#end)");

    const node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .call(drag(simulation));

    const circles = node.append("circle")
      .attr("r", d => Math.abs(d.activation))
      .attr("fill", d => d.grpColor);

    node.append("text")
        .text(function(d) {
          return d.shortName;
        })
        .attr('x', 6)
        .attr('y', 3);

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

    simulation
        .on("tick", ticked);

    function ticked() {
      link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

      node
          .attr("transform", d => `translate(${d.x}, ${d.y})`);
    }
    
    //Clear function
    if (spell == "destruction"){    
        svg.selectAll("*").remove();
        console.log("removed");
    };
        
    //var path = svg.selectAll("path"); 
    //path.exit().remove();
        
    function drag(simulation) {

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
  });
};
visualise("creation");