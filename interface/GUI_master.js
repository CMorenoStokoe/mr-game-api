function loadGUI(){
    
    /*##################
    GLOBAL VARIABLES
    ##################*/
    
    //Debug controls
    var debug_calls = 'False';
    var debug_gui_goals = 'False';
    var debug_gui_policies = 'False';
    var debug_gui_update = 'False';
    var debug_gui_intervention = 'True';
    var debug_fdg_mini = 'False';
    var debug_gui_detailView = 'False';
    var debug_update_focus = 'True';
    
    
    //GUI variables
    var numOfSliders=[1,2,3,4,5,6,7,8,9,10];
    
    
    /*##################
    MASTER FUNCTIONS
    (call slave functions)
    ##################*/
    
    function init(){
        /* Retrieve init paramaters and data */
        var ourRequest = new XMLHttpRequest();
            ourRequest.open('GET', "http://127.0.0.1:5000/init_buttons");
            ourRequest.onload = function() {
                var ourData = JSON.parse(ourRequest.responseText);
                
                if (debug_calls == 'True'){console.log(ourData)} 
                
                //Initialise GUI elements
                
                    //Home center GUI
                    groupData = ourData["btnInfo"];
                    groupData["groups"].forEach(renderGrp);
                
                    //Main sliders and text
                    statsData = ourData["statsInfo"];
                    setMainSliders(statsData[0],statsData[1],statsData[2],statsData[3]);
                    numOfSliders.forEach(renderBtnLinks);
                
                    //Main FDG
                    FDG("creation", "http://127.0.0.1:5000/simulation", "#svgMain", "normal");
                
                    //Intervention slider /*
                    document.getElementById("intvSlider").addEventListener("change", function() {
                        id=document.getElementById("intvSlider").getAttribute("data-nodeid");
                        intervene(this.getAttribute("data-nodeid"), Number(this.value));
                        if (debug_gui_intervention == 'True'){
                            
                            console.log("debug_gui_intervention: Accessed node id stored in slider: ", this.getAttribute("data-nodeid"));
            }
                    });
            }
            ourRequest.send();
    }
    init();
    
    function render(element, id){
        
        //Update either modal 1 or 2 (legacy names for left/right GUI)
        if (element == "modal1"){
            group = id;
            resetModal1();
            populateModal1(group);
            //$("#modalTmpl").modal();
            
        } else if (element == "modal2") {
            btnId = id;
            focus["id"] = $('#'+btnId).attr('data-id');
            resetModal2();
            populateModal2(btnId);
            //$("#modalTmpl2").modal();           
        }
    }
    
    function update(){
        /* Retrieve updated data */
        
        //Trigger API simulation tick
        var ourRequest = new XMLHttpRequest();
            ourRequest.open('GET', "http://127.0.0.1:5000/intervene");
            ourRequest.onload = function() {
                
            //On simulation tick update GUI
            var ourRequest = new XMLHttpRequest();
                ourRequest.open('GET', "http://127.0.0.1:5000/update");
                ourRequest.onload = function() {
                    var ourData = JSON.parse(ourRequest.responseText);

                    if (debug_calls == 'True') {console.log(ourData)};

                    nodeData = ourData["nodes"];
                    statsData = ourData["stats"];
                    groupData = ourData["groups"];

                    //Update GUI

                        //Home center GUI

                            //Sliders
                            setMainSliders(statsData[0],statsData[1],statsData[2],statsData[3]);

                            //Circle group activation colours & label
                            bundles = [];        
                            for(var i in ourData["groups"]){
                                if (ourData["groups"][i]["group"] != 'goal'){
                                    btnName = "btn-"+ourData["groups"][i]["group"];
                                    activation = ourData["groups"][i]["activation"];
                                    activColor = ourData["groups"][i]["activColor"];
                                    bundles.push({"btnName": btnName, "activColor": activColor, "activation": activation});
                                }
                            };
                            //bundles.forEach(updateGrpBtns);

                            //FDG
                            FDG("destruction", "http://127.0.0.1:5000/simulation", "#svgMain", "normal");
                            FDG("creation", "http://127.0.0.1:5000/simulation", "#svgMain", "normal");

                        //Modal 1

                            //Title
                            groupId = document.getElementById("modalTitle").innerHTML;

                            //Policy mini-progress bars 'sliders' (if modal exists)
                            group="";
                            for(var i in ourData["groups"]){
                                if(ourData["groups"][i]["group"] == groupId){
                                    group = ourData["groups"][i];
                                    populateModal1(group);
                                    break; 
                                }
                            }

                            //Goal progress

                            for(var i in ourData["groups"]){
                                if(ourData["groups"][i]["group"] == 'goal'){
                                    ourData["groups"][i]['nodes'].forEach(setGoalProgs)
                                    populateModal1(group);

                                    if (debug_gui_update == 'True') {console.log("debug_gui_update: Calling goal progress bar update method with payload: ", ourData["groups"][i]['nodes'])}
                                }
                            }

                        //Modal 2

                            //Pop vis
                            id = focus["id"];
                            for(var i in ourData["nodes"]){
                                if(ourData["nodes"][i]["id"] == id){
                                    //funding = ourData["nodes"][i]["funding"];
                                    focus_value = ourData["nodes"][i]["activation"];
                                    focus_fundLvl = ourData["nodes"][i]["currIntvLvl"];
                                    setIntvSlider(focus_fundLvl);
                                    setPopVis(focus_value);
                                    break; 
                                }
                            }
                    };
                    ourRequest.send();
            }
            ourRequest.send();
        
        
        
        if (debug_gui_update == 'True') {console.log("update");}
    }
    
    var timerCallCount = 0
    function chrono(time){
        
        //If reset/stop command called then clear timer imediately
        if (time == "stop"){
            clearInterval(timer);
            timerCallCount = -1;
            
            if (debug_gui_update == 'True') {console.log("timer stopped");}
        
        //If timer not active then start timer 
        } else if (timerCallCount == 0){
            timer = setInterval(function() {update();}, time)
            
            if (debug_gui_update == 'True') {console.log("timer set");}
        
        //If timer already active then pass
        } else {
            return;
        }
        
        //Increment count to indicate timer was requested to start
        timerCallCount++;
    };

    /*##################
    SLAVE FUNCTIONS 
    (called by master functions)
    ##################*/
    
    //PERSISTANT HOME: CENTER UI
    function renderGrp(group){
        
        /* For policy node group, create drop-down button */
        if (group["group"] == "ENABLED"){
            
            //Compose button IDs
            btnName = "btn-"+group["group"]; //modalId = "#modal-"+group["group"];
            
            //Create html for alert badge within button
            btnHTML =  group["group"]+"<br>"+"<span class=\"badge badge-danger btnAlert\" id=\""+btnName+"-alert\">"+group["activation"].toFixed(0)+"</span>";
            
            //Create button element
            var btn = document.createElement("BUTTON");
            btn.id = btnName;
            btn.className = "btn btn-light grpBtn";
            btn.innerHTML = btnHTML;
            btn.setAttribute("data-toggle", "dropdown");
            
            //Append created button to GUI location in drop-down div
            document.getElementById("div-dropdown").appendChild(btn); 
            
            //Add function to created button using event listener 
            document.getElementById(btnName).addEventListener("click", function(e) {   
                render("modal1",group);
                $('.dropdown-toggle').dropdown();
                
                update();
            });
            
            //Show alert badge if total activation of nodes in group is high
            if (group["activation"] >= 100){
                document.getElementById(btnName+'-alert').style.visibility = "visible";
            }
        
        }
        
        /* For goal node group create a progress bar for each node within group */
        if (group["group"] == "goal"){
            
            //For each node in goal group render a progress bar
            group["nodes"].forEach(renderGoalProgs);
            
            if (debug_gui_goals == 'True'){console.log("debug_gui_goals: Goals group identified, attempting to call renderGoalProgs");}
        }
    }
    
    var goalProgCount = 1;
    function renderGoalProgs(node){
        
        if (debug_gui_goals == 'True'){console.log("debug_gui_goals: Called renderGoalProgs with payload: ", node);}
        
        //Currently only supports 10 goals, if this method is called more, then pass to prevent throwing error on not being able to find progress bar template #11 etc.
        if (goalProgCount <= 10) {
            
            //Get template progress bar objects to adapt for each goal
            div = document.getElementById("goalProgDiv"+goalProgCount);
            title = document.getElementById("progress_txt_goal"+goalProgCount);
            bar = document.getElementById("progress_bar_goal"+goalProgCount);
            barTxt = document.getElementById("progress_barTxt_goal"+goalProgCount);
            
            if (debug_gui_goals == 'True'){console.log("debug_gui_goals: Got template elements: ",div,title,bar,barTxt);}
            
            //Make new IDs specific to goals in simulation data based on the goal's ID so it can be easily called later with only the goal ID
            nodeId_safe = node['id'].replace(/ /g, "_");
            divId_new = "progress_div_" + nodeId_safe;
            titleId_new = "progress_txt_" + nodeId_safe;
            barId_new = "progress_bar_" + nodeId_safe;
            barTxtId_new = "progress_barTxt_" + nodeId_safe;
            
            if (debug_gui_goals == 'True'){console.log("debug_gui_goals: Made new IDs: ",divId_new,titleId_new,barId_new,barTxtId_new);}
            
            //Replace template IDs with new IDs
            div.id = divId_new;
            title.id = titleId_new;
            bar.id = barId_new;
            barTxt.id = barTxtId_new;
            
            //Set permanent information
            title.innerText = node["shortName"];
            
            if (debug_gui_goals == 'True'){console.log("debug_gui_goals: Set bar title: ", node["shortName"]);}

            //Get progress bar with new ID and move from hiding to GUI location
            div_new = document.getElementById(divId_new);
            document.getElementById("goalsDiv").appendChild(div_new);

            //Use update method to set starting values
            setGoalProgs(node);
            
        }
        else if (goalProgCount >= 11){
            console.log("WARNING: Over 10 goals detected, not all are displayed");
        }
        
        //Increment count for the next time this method is called
        goalProgCount ++;
    }
    
    function setGoalProgs(node){
        
        //Get goal progress bar and in-bar text
        nodeId_safe = node['id'].replace(/ /g, "_")
        
        bar = document.getElementById("progress_bar_"+nodeId_safe);
        barTxt = document.getElementById("progress_barTxt_"+nodeId_safe);
        
        //Get activation of node to set the fill of the progress bar
        activation = Number(node["activation"])
        
        //Assign progress color
        if (activation > 100 || activation < 0){
            color = "black";
        } else if (activation < 25) {
            color = "green";
        } else if (activation > 50) {
            color = "orange";
        } else if (activation > 75) {
            color = "red";       
        }
        
        //Update value and color for progress bar, text for in-bar text
        $(bar).css('width', activation+"%").attr('aria-valuenow', activation);
        $(bar).css('background-color', color);         
        $(barTxt).text(activation.toFixed(0));
        
        if (debug_gui_goals == 'True'){
            console.log("debug_gui_goals: Called setGoalProgs with payload: ", node);
            console.log("debug_gui_goals: Goal id found: ", node['id']);
            console.log("debug_gui_goals: Goal progress value set: ", $(bar).css('width'), $(bar).attr('aria-valuenow'));
            
        }
    }
    
    function setMainSliders(total, goal, goalPct, totalPct){
        
        totalRnd = Number(total);
        totalPctRnd = Number(totalPct);
        goalPctRnd = Number(goalPct);
        $('#progress_total').css('width', totalPctRnd.toFixed(2)+"%").attr('aria-valuenow', totalPctRnd.toFixed(2));
        $('#progress_totalTxt').text(totalRnd.toFixed(0));
        $('#progress_goal').css('width', goalPctRnd.toFixed(2)+"%").attr('aria-valuenow', goalPctRnd.toFixed(2));
        $('#progress_goalTxt').text(goal);
        $('#progress_goalVal').text(goalPctRnd.toFixed(0));
        
    }
    
    function updateGrpBtns(bundle){
        
        btnId = '#'+bundle["btnName"];
        btnAlertId = bundle["btnName"]+'-alert';
        color = bundle["activColor"];
        activation = bundle["activation"];
        //{%}Dynamic values bookmark
        if (activation >= 100 || activation < 10){
            document.getElementById(btnAlertId).style.visibility = "visible";
        } else {
            document.getElementById(btnAlertId).style.visibility = "hidden";
        }

        activationRnd = Number(activation);
        text = activationRnd.toFixed(0);
        $('#'+btnAlertId).text(text);
        $('#'+btnAlertId).css('background-color', color);
    }
    
    /*
    function colorGrp(bundle){
        //Color
        btnId = '#'+bundle["btnName"];
        color = bundle["activColor"];
        activation = bundle["activation"];
        $(btnId).css('background-color', color);
        
        //Text
        activationRnd = Number(activation);
        groupname = bundle["btnName"].replace('btn-','');
        html = groupname+"<br>"+activationRnd.toFixed(0);
        $(btnId).html(html);
    }
    */
    
    //MODAL 1: RENDER & RESET
    var sliderCount = 1;
    function populateModal1(group){
        document.getElementById("modalTitle").innerHTML = group["group"];
        sliderCount = 1;
        group["nodes"].forEach(setSlider);
    };
    
    function setSlider(node){
        
        //Set progress bars for up to 10 nodes per group e.g., policies
        if (sliderCount <= 10) {
            
            btnId = "#slider"+sliderCount+"Txt";
            progressId = "#slider"+sliderCount;
            progressTextId = "#slider"+sliderCount+"Curr";
            sliderDiv =  document.getElementById("div-slider"+sliderCount);
            progressVal = Number(node["activation"]);
            
            if (debug_gui_policies == 'True') {console.log("debug_gui_miniProgs: Got progress element: ", sliderDiv);}
            
            //Assign progress color
            if (progressVal > 100 || progressVal < 0){
                color = "black";
            } else if (progressVal > 75 || progressVal < 25){
                color = "red";
            } else if (progressVal > 60 || progressVal < 40) {
                color = "orange";
            } else {
                color = "green";       
            }

            $(progressId).css('width', progressVal.toFixed(2)+"%").attr('aria-valuenow', progressVal.toFixed(2));
            $(progressId).css('background-color', color); 
            $(progressTextId).text(progressVal.toFixed(0));
            $(btnId).text(node["shortName"]);

            $(btnId).attr('data-id', node["id"]);
            $(btnId).attr('data-activation', node["activation"]);
            $(btnId).attr('data-currIntvLvl', node["currIntvLvl"]);

            document.getElementById("dropdown-menu").appendChild(sliderDiv);
        
        }
        
        //If more than 10
        else if (sliderCount >= 11) {
            console.log("WARNING: Over 10 policies detected in this group, not all are displayed");
        }
        
        sliderCount ++;
    }

    function resetModal1(){
        numOfSliders.forEach(resetSliders);
    }
    
    function resetSliders(sliderCount){
        sliderDiv =  document.getElementById("div-slider"+sliderCount);
        document.getElementById("hiddenItems").appendChild(sliderDiv);
    }
    
    //MODAL2: RENDER & RESET    
    function populateModal2(btnId){
        
        //Get stats for currently viewed trait from memory in their button
        nodeId = document.getElementById(btnId).getAttribute('data-id');
        nodeName = document.getElementById(btnId).innerText;
        nodeIntvLvl = document.getElementById(btnId).getAttribute('data-currIntvLvl');
        
        focus['id']=nodeId;
        focus['shortName']=nodeName;
        
        //Set title and subtitle
        document.getElementById("modal2Title").innerHTML = nodeName;
        document.getElementById("modal2Title").setAttribute('data-btnId', btnId);
        document.getElementById("modal2Subtitle").innerHTML = nodeId;
        
        //Set sliderBtn data-id
        document.getElementById("intvSlider").setAttribute('data-id', nodeId);
        
        //Set intv slider
        setIntvSlider(nodeIntvLvl);
        
        //Set pop vis
        progressTxtId = '#'+btnId.replace('Txt','')+"Curr";
        focus_value = $(progressTxtId).html();
        setPopVis(focus_value);
        
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
        
        //Make right panel elements visible after first call of this method
        document.getElementById("rightHeader").style.visibility = "visible";
        document.getElementById("rightBody").style.visibility = "visible";
        document.getElementById("rightFooter").style.visibility = "visible";
    }
    
    function setPopVis(focus_value){
        number = Math.floor(focus_value/10);
        percent = focus_value+'%'
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
        
        resetPops();
        colorPops(number);
        
        prevalence_displaySafe = Number(focus_value)
        
        if (debug_gui_detailView == 'True'){
            console.log("debug_gui_detailView: Currently viewed trait activation level ", prevalence_displaySafe.toFixed(2));
        }
        
        document.getElementById("prevalenceTxt").innerText = prevalence_displaySafe.toFixed(2);
    }
    
    function renderFdgTxt(nodeId){
        var ourRequest = new XMLHttpRequest();
            URL = "http://127.0.0.1:5000/simulation/"+nodeId
            ourRequest.open('GET', URL);
            ourRequest.onload = function() {
                var ourData = JSON.parse(ourRequest.responseText);
                
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
                
            }
            ourRequest.send();
    }
    
    function renderBtnLinks(id){
        btnId = "slider"+id+"Txt";
        document.getElementById(btnId).addEventListener("click", function() {
            render("modal2",this.id);
        });
    }
    
    function setIntvSlider(focus_intv){
        intvSlider =  document.getElementById("div-intvSlider");
        
        header = document.getElementById("intvSliderHider").appendChild(intvSlider);
        
        $('#intvSlider').attr('value', focus_intv);
        document.getElementById("intvSlider").value = focus_intv
        document.getElementById("intvSliderValue").value = focus_intv
        
        header = document.getElementById("rightHeader").appendChild(intvSlider); 
    }
    
    function resetModal2(){
        document.getElementById("effectors").innerHTML = "";
        document.getElementById("effecteds").innerHTML = "";
    }
 
    function intervene(target, funding){
        
        if (funding < 0){
            valence = '-';
        }else if (funding >= 0){
            valence = '+';
        }
        value = Math.abs(funding * 10);
        
        var xhr = new XMLHttpRequest();        

            xhr.open("POST", "http://127.0.0.1:5000/intervene", 'True');
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    //Redraw views
                    //update(["centerGUI","modal1","modal2"]);
                    
                    //chrono(5000);
                    //if (debug_gui_intervention == 'True') {console.log("intervention");}
                }
            }
            xhr.send(JSON.stringify({
                                        "id": target,
                                        "valence": valence,
                                        "value": value,
            }));
    }
    
    //Global buttons
    //Reset 
    var btn_reset = document.getElementById("btn_reset");
    btn_reset.addEventListener("click", function() {
        resetRequest = new XMLHttpRequest();
        resetRequest.open('GET', "http://127.0.0.1:5000/reset");
        resetRequest.onload = function(){
            //chrono("stop");
        };
        resetRequest.send();
    })
    //End turn
        //GLOBAL BUTTON: RESET 
    var btn_endTurn = document.getElementById("btn_endTurn");
    btn_endTurn.addEventListener("click", function() {
        update();
    })
    

};

window.onload=loadGUI()