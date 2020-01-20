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
    nodeIntvLvl = node['currIntvLvl'];
    nodeActivation = node['activation'];
    
    if (debug_update_focus == 'True'){
            console.log("debug_update_focus: populateModal2_alt function called, now delegating tasks with extracted data: ",nodeId,nodeName,nodeIntvLvl);
    }

    //Set title and subtitle
    document.getElementById("modal2Title").innerHTML = nodeName;
    document.getElementById("modal2Subtitle").innerHTML = nodeId;

    //Set intv slider
    setIntvSlider_alt(nodeIntvLvl, nodeId);

    //Set pop vis
    setPopVis_alt(nodeActivation);
    
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

function setPopVis_alt(nodeActivation){
    
    if (debug_update_focus == 'True'){
            console.log("debug_update_focus: setPopVis method called with payload: ",nodeActivation);
    }
    
    activation_pops = Math.floor(nodeActivation/10);
    activation_pct = nodeActivation+'%'
    
        function resetPops(){
            count = 1;
            while (count <= 10) {
                document.getElementById("prevPop"+count).style.color = "black";
                count++;
            } 
        }
    
        function colorPops(affected){
            while (affected >= 1) {
                $('#prevPop'+affected).css('color', 'red');
                affected--;
            }
        }
    
    document.getElementById("prevalenceTxt").innerText = activation_pct;
    
    resetPops();
    colorPops(activation_pops);

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

            function scribe (link){
                //Identify whether link affects, or is affected by, the node
                if (link["source"] == nodeId){
                    txtDiv = document.getElementById("effectors");
                    node = link["target"];
                    if (effectors_done.includes(node)){
                        link["color"]="";
                    }   
                    effectors_done.push(link["target"]);
                }
                else if (link["target"] == nodeId){
                    txtDiv = document.getElementById("effecteds");
                    node = link["source"];
                    if (effecteds_done.includes(node)){
                        link["color"]="";
                    }
                    effecteds_done.push(link["source"]);
                }


                //Render HTML
                if (link["color"] == "blue"){
                    html = "<span style=\"color:blue\"><i class=\"fas fa-chevron-circle-down\"></i>"+node+"</span><br>";
                } else if (link["color"] == "red"){
                    html = "<span style=\"color:red\"><i class=\"fas fa-chevron-circle-up\"></i>"+node+"</span><br>";
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