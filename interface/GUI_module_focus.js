//Debug console
var debug_update_focus = 'False';

//FDG visualisation - GUI Cross-talk functions

    //Alternative render function - if using node ID rather than button ID, use alt update method for modal 2 i.e., rendering focus view right-hand panel from visualisation using node attributes such as ID, rather than relying on stored info in trait buttons
function render_alt(element, id){
        
        var ourRequest = new XMLHttpRequest();
    
            URL = "http://127.0.0.1:5000/simulation/singleNode/" + id
            
            if (debug_update_focus == 'True'){
                console.log("debug_update_focus: render_alt function called and API request made to: ", URL);
            }
            
            ourRequest.open('GET', URL);
            ourRequest.onload = function() {
                
                var ourData = JSON.parse(ourRequest.responseText);
                populateModal2_alt(ourData)                
                
                if (debug_update_focus == 'True'){
                    console.log("debug_update_focus: API request loaded: ", ourData);
                }
            };
            ourRequest.send();               
}

function getData(ourRequest) {
    var ourData = JSON.parse(ourRequest.responseText);
    populateModal2_alt(ourData)

    if (debug_update_focus == 'True'){
        console.log("debug_update_focus: API request loaded: ", ourData);
    }
}

function populateModal2_alt(node){

    //Get stats for currently viewed trait from memory in their button
    nodeId = node['id']
    nodeName = node['shortName']
    nodeMRBaseId = node['id_MRBase']
    nodeIntvLvl = node['currIntvLvl'];
    nodeActivation = node['activation'];
    nodeUnits = node["units"];
    
    if (debug_update_focus == 'True'){
            console.log("debug_update_focus: populateModal2_alt function called, now delegating tasks with extracted data: ",nodeId,nodeName,nodeIntvLvl);
    }

    //Set title and subtitle
    document.getElementById("modal2Title").innerHTML = nodeName;
    document.getElementById("modal2Subtitle").innerHTML = nodeId + '<br> ID: ' + nodeMRBaseId;
    document.getElementById("unitsTxt").innerText = nodeUnits;

    //Set intv slider
    setIntvSlider_alt(nodeIntvLvl, nodeId);

    //Set pop vis
    setPopVis_alt(node);
    
    //Right mini text read-out of FDG
    renderFdgTxt_alt(nodeId)
    
    /*
    //Right mini FDG      
    URL = "http://127.0.0.1:5000/simulation/" + nodeId;        
    FDG("destruction", URL, "#svgM2", "compact");
    FDG("creation", URL,"#svgM2", "compact");
    renderFdgTxt(nodeId);

    //Debug console
    if (debug_fdg_mini == 'True'){
        console.log("debug_fdg_mini: URL for calling API assembled: ", URL);
        console.log("debug_fdg_mini: FDG destroyed: ", FDG("destruction", URL, "#svgM2", "compact"));
        console.log("debug_fdg_mini: FDG created: ", FDG("creation", URL, "#svgM2", "compact"));
    }
    */
    
    //Make right panel elements visible after first call of this method
    document.getElementById("rightHeader").style.visibility = "visible";
    document.getElementById("rightBody").style.visibility = "visible";
    document.getElementById("rightFooter").style.visibility = "visible";
}


function setIntvSlider_alt(nodeIntvLvl, nodeId){
    
    if (debug_update_focus == 'True'){
            console.log("debug_update_focus: setIntvSlider method called with payload: ",nodeIntvLvl);
    }
    
    intvSlider =  document.getElementById("div-intvSlider");

    header = document.getElementById("intvSliderHider").appendChild(intvSlider);

    $('#intvSlider').attr('value', nodeIntvLvl);
    document.getElementById("intvSlider").value = nodeIntvLvl
    document.getElementById("intvSliderValue").value = nodeIntvLvl
    
    $('#intvSlider').attr('data-nodeid', nodeId);

    header = document.getElementById("rightHeader").appendChild(intvSlider); 
}

function setPopVis_alt(node){
    
    //Parse variables from payload
    activation = node['activation'];
    units = node['units'];
    units_type = node['units_type'];
    min = node['activation_min'];
    max = node['activation_max'];
    
    //Compute inferred variables
    activation_pct = activation/max*100;
    activation_pops = Math.floor(activation_pct/10);
   if (node["units_type"] == "binary") {
            activation_pct = activation*100
            if (activation_pct >=100) {
                activation_text = activation_pct.toFixed(0)+'%';
            } else if (activation_pct >=1) {
                activation_text = activation_pct.toFixed(1)+'%';
            } else if (activation_pct >=0.1){
                activation_text = activation_pct.toFixed(2)+'%';
            } else if (activation_pct >=0.01){
                activation_text = activation_pct.toFixed(3)+'%';
            } else {
                activation_text = activation_pct.toFixed(4)+'%';
            }
        } else {
            if (activation >=100) {
                activation_text = activation.toFixed(0);
            } else if (activation >=0.1) {
                activation_text = activation.toFixed(1);
            } else if (activation >=0.01){
                activation_text = activation.toFixed(2);
            } else if (activation >=0.001){
                activation_text = activation.toFixed(3);
            } else {
                activation_text = activation.toFixed(4);
            }
    }
    
    if (debug_update_focus == 'True'){
            console.log("debug_update_focus: setPopVis method called with payload: ",node);
            console.log("debug_update_focus: calculated from activation: activation_pct and activation_pops: ", activation, activation_pct, activation_pops);
    }
    
    //Function to reset pops display
    function resetPops(){
        count = 1;
        while (count <= 10) {
            document.getElementById("prevPop"+count).style.color = "black";
            count++;
        } 
    }
    
    //Function to set pops display
    function colorPops(affected){
        while (affected >= 1) {
            $('#prevPop'+affected).css('color', 'red');
            affected--;
        }
    }
       
    //Set pop display
    resetPops();
    colorPops(activation_pops);
    
    //Set text to display on trait focus
    document.getElementById("prevalenceTxt").innerText = activation_text;
    document.getElementById("prevalenceTxt_min").innerText = min;
    document.getElementById("prevalenceTxt_max").innerText = max;

}

function renderFdgTxt_alt(nodeId){
    
    if (debug_update_focus == 'True'){
            console.log("debug_update_focus: renderFdgTxt method called with payload: ", nodeId);
    }
    
    var ourRequest = new XMLHttpRequest();
        URL = "http://127.0.0.1:5000/simulation/"+nodeId
        ourRequest.open('GET', URL);
        ourRequest.onload = function() {
            var ourData = JSON.parse(ourRequest.responseText);
            
            //clean slate before writing
            reset()
            
            effectors_done=[nodeId,];
            effecteds_done=[nodeId,];
            ourData["links"].forEach(scribe);

            function scribe(link){
                //Identify whether link affects, or is affected by, the node
                if (link["source"] == nodeId){
                    txtDiv = document.getElementById("effectors");
                    node = link["target"];
                    image = "<img src=\"" + link["target_iconId"] + " \"style=\" height:35px; width:35px; \" >"
                    if (effectors_done.includes(node)){
                        link["color"]="";
                    }   
                    effectors_done.push(link["target"]);
                }
                else if (link["target"] == nodeId){
                    txtDiv = document.getElementById("effecteds");
                    node = link["source"];
                    image = "<img src=\"" + link["source_iconId"] + " \"style=\" height:35px; width:35px; \" >"
                    if (effecteds_done.includes(node)){
                        link["color"]="";
                    }
                    effecteds_done.push(link["source"]);
                }


                //Render HTML
                if (link["color"] == "blue"){
                    html = "<span style=\"color:blue\"><i class=\"fas fa-chevron-circle-down\"></i>"+image+"</span><br>";
                } else if (link["color"] == "red"){
                    html = "<span style=\"color:red\"><i class=\"fas fa-chevron-circle-up\"></i>"+image+"</span><br>";
                } else {
                    return;   
                }
                txtDiv.innerHTML += html;
            }
            
            function reset(){
                txtDiv = document.getElementById("effectors");
                txtDiv.innerHTML = " ";
                txtDiv2 = document.getElementById("effecteds");
                txtDiv2.innerHTML = " ";
            }

        }
        ourRequest.send();
}