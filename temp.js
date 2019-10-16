model_propagation = {

//Intitalise variables
  var TESTvalue = "no activation";
  var TESTvalue2 = "no propagation";
  var TESTvalues = [];
  
  var selector_nodes = data["nodes"]; //selects nodes in data
  var selector_links = data["links"]; //selects links in data
  var scouted = [];
  var scouted_links = [];
  var intv_strg = 1; //Intervention strength

//Declare functions  
  function activator(nodeID,weight){
    for(var i in selector_nodes){
      if(selector_nodes[i].id == nodeID){
        selector_nodes[i].activation += weight; //Increase activation of selected node
        TESTvalue = selector_nodes[i].activation; //TEST:if output is activation level, success
        break;
      };
    };
  };
  
  function activator2(nodeID,weight){
    for(var i in selector_nodes){
      if(selector_nodes[i].id == nodeID){
        if(weight >= 0){
          selector_nodes[i].activation *= weight; //Increase activation of node according to beta weight w/origin node
          TESTvalues += selector_nodes[i].activation;
        }
          if(weight <= 0){
          selector_nodes[i].activation /= Math.abs(weight); //Increase activation of node according to beta weight w/origin node
          TESTvalues += selector_nodes[i].activation;
        }
        TESTvalue2 = selector_nodes[i].activation; //TEST:if output is activation level, successful propagation
        break;
      };
    };
  };

  function scout(nodeID){
    scouted = [];
    scouted_links = [];
    for(var i in selector_links){
      if(selector_links[i].source == nodeID){
        scouted.push(selector_links[i].target);
        scouted_links.push(selector_links[i].value);
      };
    };
  };
  
  function intervene(nodeID){
    activator(nodeID,intv_strg);
    scout(nodeID);
    for (var i in scouted){
      activator2(scouted[i],scouted_links[i]);
    }
  };
  
  function reset(){
    for(var i in selector_nodes){
      selector_nodes[i].activation = 1; //reset activation of selected node
      //TESTvalues  += selector_nodes[i].activation;
    }
  };
 
  function resetOne(nodeID){
    for(var i in selector_nodes){
      if(selector_nodes[i].id == nodeID){
        selector_nodes[i].activation = 1; //reset activation of selected node
        //TESTvalue = selector_nodes[i].activation; //TEST:if output is activation level, success
        break;
      };
    };
  };  
  
//Call functions
  //activator("Gout");  
  //scout("Years of schooling");
  intervene("Years of schooling");
  //reset();
  //resetOne("Gout");

//Return test value
  return {
  "TESTvalue":TESTvalue,
  "TESTvalue2":TESTvalue2,
  "TESTvalues":TESTvalues,
  "selector_nodes":selector_nodes,
  "selector_links":selector_links,
  "scouted":scouted,
  "scouted_links":scouted_links,
  "intv_strg":intv_strg,
  };
}
