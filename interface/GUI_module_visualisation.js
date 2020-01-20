// Global variables (sorry)
arrowColorStatus='#999'
function toggleArrows(){
    if(arrowColorStatus=='#999'){
        arrowColorStatus='none';
    } else if(arrowColorStatus=='none'){
        arrowColorStatus='#999';
    };
}
//Listen out for view button(s) being pressed to change FDG view
document.getElementById('btn_toggleArrows').addEventListener("click", function(e) {   
    toggleArrows();
    console.log(arrowColorStatus);
});

//Force-directed graph function (builder for both main and mini-fdgs)
function FDG (spell,URL,svgId,view) {
    
    //Debug controls
    var debug_visualisation = 'False';
    
    //Select SVG DOM element
    const svg = d3.select(svgId),
    width = +svg.attr("width"),
    height = +svg.attr("height");
    
    if (debug_visualisation == 'True'){
        console.log("debug_visualisation: FDG function called with payloads: ", spell,URL,svgId,view);
        console.log("debug_visualisation: SVG id selected: ", d3.select(svgId));
    }
    
    //Views - set scale factors and classes
    var graphCohesion = -2000;
    var edgeWidth = 1;
    var fontSize = "18px";
    var textShadowClass = "shadow_v_normal";
    var scaleFactor = 0.75;
    var circleRadius = 5*scaleFactor;
    var arrowPlacement = circleRadius*7*scaleFactor*2; circleRadius*7;
    var arrowSize = circleRadius*2*scaleFactor;
    var arrowColor = arrowColorStatus;
    if (view=="collapsed"){
        graphCohesion = -5000;
        edgeWidth = 5;
        fontSize = "30px";
        textShadowClass = "shadow_v_collapsed";
        circleRadius = 2;
        arrowPlacement = circleRadius*7;
        arrowSize = circleRadius*2;
        arrowColor = '#999';
    };
    if (view=="compact"){
        graphCohesion = -800;
        edgeWidth = 2;
        fontSize = "18px";
        textShadowClass = "shadow_v_compact";
        circleRadius = 1;
        arrowPlacement = circleRadius*7;
        arrowSize = circleRadius*2;
        arrowColor = '#999';
    };
    
    /*setTimeout(function() {
      //your code to be executed after 1 second
    }, 200);
    */
    let dataPromise = d3.json(URL);
    
    if (debug_visualisation == 'True'){
        console.log("debug_visualisation: Data promise made: ", d3.json(URL))
    }

    dataPromise.then(function draw(data) {

    //const color = d3.scaleSequential(d3.interpolatePiYG);
    //d3.scaleOrdinal(d3.schemeCategory10);
    const links = data.links.map(d => Object.create(d));
    const nodes = data.nodes.map(d => Object.create(d));
        
    if (debug_visualisation == 'True'){
        console.log("debug_visualisation: Link data selected: ", data.links);
        console.log("debug_visualisation: Node data selected: ", data.nodes);
    }

// Set up simulation 
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(graphCohesion))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    const link = svg.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(links, d => d.id)
      .join(
        enter => enter.append("line")
          .attr("stroke-width", edgeWidth)
          .attr("stroke", d => d.color)//edge color as function of beta weight sign//
          .attr("stroke-opacity", d => 0.1 + Math.abs(d.value))//edge opacity as function of beta weight value//
          .attr("marker-end", "url(#end)"),
        /*
        update => update
          .attr("stroke", d => "black")
         .call(update => update.transition(t)
            .attr("x", (d, i) => i * 16)),
        exit => exit
         .call(exit => exit.transition(t)
            .remove())
        */
      );

    const node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(nodes)
      .join(
        enter => enter.append("g")
        )
      .call(drag(simulation));

    const circles = node.append("circle")
      .attr("r", 5 * circleRadius) //d => Math.abs(d.activation)*circleRadius
      .attr("stroke", d => d.grpColor)
      .attr("fill", d => d.activColor)
      .attr("dataHolder", d => d.id)
      .on("click", function(){
          render_alt("modal2_alt",this.getAttribute("dataHolder"));
      });

    node.append("text")
        .text(function(d) {
          return d.shortName;
        })
        .attr("class", textShadowClass)
        .style("font-size", fontSize)
        .attr("text-anchor", "middle")
        .attr('x', 6)
        .attr('y', 3);
        
    // From https://stackoverflow.com/questions/28050434/introducing-arrowdirected-in-force-directed-graph-d3
    svg.append("svg:defs").selectAll("marker")//edge color as function of beta weight sign//
        .data(["end"])      // Different link/path types can be defined here
        .enter().append("svg:marker")    // This section adds in the arrows
        .attr("id", String)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", arrowPlacement) // original val: 15
        .attr("refY", -1.5) // original val: -1.5
        .attr("markerWidth", arrowSize)  // original val: 5
        .attr("markerHeight", arrowSize) // original val: 5
        .attr("stroke", arrowColor)
        .attr("fill", arrowColor) // original val: '#999'
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", "M0,-5L10,0L0,5");

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
