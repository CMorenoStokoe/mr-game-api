function loadGUI(){
    
    var numOfSliders=[1,2,3,4,5,6,7,8,9,10];
    var focus = {'id':null,'shortName':null,'activation':null,'funding':null, 'currIntvLvl':null};
    
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
                    intervene(focus["id"], Number(this.value));
                });
            }
            ourRequest.send();
    }
    init();
    
    function render(element, id){
        //Update either modal 1 or 2
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
        
        var ourRequest = new XMLHttpRequest();
            ourRequest.open('GET', "http://127.0.0.1:5000/update");
            ourRequest.onload = function() {
                var ourData = JSON.parse(ourRequest.responseText);

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
                            btnName = "btn-"+ourData["groups"][i]["group"];
                            activation = ourData["groups"][i]["activation"];
                            activColor = ourData["groups"][i]["activColor"];
                            bundles.push({"btnName": btnName, "activColor": activColor, "activation": activation});
                        };
                        bundles.forEach(updateGrpBtns);
                        //bundles.forEach(colorGrp);
                        //FDG
                        FDG("destruction", "http://127.0.0.1:5000/simulation", "#svgMain", "normal");
                        FDG("creation", "http://127.0.0.1:5000/simulation", "#svgMain", "normal");
                    //Modal 1
                        //Title
                        groupId = document.getElementById("modalTitle").innerHTML;
                        //Sliders (if modal exists)
                        group="";
                        for(var i in ourData["groups"]){
                            if(ourData["groups"][i]["group"] == groupId){
                                group = ourData["groups"][i];
                                populateModal1(group);
                                break; 
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
        console.log("update")
    }
    
    var timerCallCount = 0
    function chrono(time){
        if (time == "stop"){
            clearInterval(timer);
            console.log("timer stopped")
            timerCallCount = -1;
        } else if (timerCallCount == 0){
            timer = setInterval(function() {update();}, time)
            console.log("timer set")
        } else {
            pass;
        }
        timerCallCount++;
    };

    /*##################
    SLAVE FUNCTIONS 
    (called by master functions)
    ##################*/
    
    //PERSISTANT HOME: CENTER UI
    function renderGrp(group){
        /*create div holding group of buttons*/
        btnName = "btn-"+group["group"];
        btnHTML =  group["group"]+"<br>"+"<span class=\"badge badge-danger btnAlert\" id=\""+btnName+"-alert\">"+group["activation"].toFixed(0)+"</span>";
            
        modalId = "#modal-"+group["group"];
        var btn = document.createElement("BUTTON");
        btn.id = btnName;
        btn.className = "btn btn-light grpBtn";
        btn.innerHTML = btnHTML;
        btn.setAttribute("data-toggle", "dropdown");
        
        document.getElementById("div-dropdown").appendChild(btn); 
        //document.getElementById(btnName).style.border = "1px solid "+group["grpColor"];
        document.getElementById(btnName).addEventListener("click", function(e) {   
            render("modal1",group);
            //update(["centerGUI","modal1"]);
            $('.dropdown-toggle').dropdown();
        });
        
        if (group["activation"] >= 100){
            document.getElementById(btnName+'-alert').style.visibility = "visible";
        }
            
        
        //bundle = {"btnName":btnName,"activColor":group["activColor"],"activation":group["activation"]};
        //colorGrp(bundle);
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
        
        btnId = "#slider"+sliderCount+"Txt";
        progressId = "#slider"+sliderCount;
        progressTextId = "#slider"+sliderCount+"Curr";
        sliderDiv =  document.getElementById("div-slider"+sliderCount);
        progressVal = Number(node["activation"]);
        
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
        
        //Set FDG      
        URL = "http://127.0.0.1:5000/simulation/" + nodeId;
        FDG("destruction", URL, "#svgM2", "compact");
        FDG("creation", URL,"#svgM2", "compact");
        renderFdgTxt(nodeId);
        
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
        
        document.getElementById("prevalenceTxt").innerText = percent;
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

            xhr.open("POST", "http://127.0.0.1:5000/intervene", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    //Redraw views
                    //update(["centerGUI","modal1","modal2"]);
                    chrono(3000);
                    console.log("intervention")
                }
            }
            xhr.send(JSON.stringify({
                                        "id": target,
                                        "valence": valence,
                                        "value": value,
            }));
    }
    
    //depreciated button code 
    /*
    //BUTTON: INTERVENE    
       function setIntvBtns(btnId){
        btn = document.getElementById(btnId);
        btn.onclick = function(){
        me = document.getElementById(this.id);
            target = me.getAttribute('data-id');
            valence = me.getAttribute("data-vale");
            value = me.getAttribute("data-value");
            
            //Send intervention request to API
                   
        };
    }
    var intvBtnIds=["btn-intv+","btn-intv-"];
    intvBtnIds.forEach(setIntvBtns);
    */
    
    //GLOBAL BUTTON: RESET 
    var btn_reset = document.getElementById("btn_reset");
    btn_reset.addEventListener("click", function() {
        resetRequest = new XMLHttpRequest();
        resetRequest.open('GET', "http://127.0.0.1:5000/reset");
        resetRequest.onload = function(){
            chrono("stop");
        };
        resetRequest.send();
    })
    

};

window.onload=loadGUI()