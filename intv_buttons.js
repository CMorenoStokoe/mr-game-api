window.onload=function(){
 
    var btn_intervention = document.getElementById("btn_intervention");
    var form_intervention = document.getElementById("form_intervention");
    
    var btn_reset = document.getElementById("btn_reset");
    btn_reset.addEventListener("click", function() {
        var ourRequest = new XMLHttpRequest();
            ourRequest.open('GET', "http://127.0.0.1:5000/reset");
            ourRequest.send();
    })
                               
    /* Retrieve nodes in data */
    var ourRequest = new XMLHttpRequest();
        ourRequest.open('GET', "http://127.0.0.1:5000/init_buttons");
        ourRequest.onload = function() {
            var ourData = JSON.parse(ourRequest.responseText);
            console.log(ourData["groups"])
            ourData["groups"].forEach(renderGrp);
        };
        ourRequest.send();
    
    /* Automatically create buttons for nodes in data */
    function renderGrp(group){
        /*create div holding group of buttons*/
        divName = "div-"+group["group"];
        divHTML = "<strong>"+group["group"]+"<strong>";
        var div = document.createElement("SPAN");
        div.id = divName;
        div.className = "div-grp, card";
        div.innerHTML = divHTML;
        document.getElementById("view-right").appendChild(div); 
        document.getElementById(divName).style.backgroundColor = group["grpColor"];
        group["nodes"].forEach(renderBtn);
    }
    
    function renderBtn(node){
        /*create span holding buttons */
        divName = "div-"+node["group"];
        spanName = "span-"+node["id"];
        spanHTML = "<strong>"+node["shortName"]+"<br>"+"<strong>";
        var span = document.createElement("SPAN");
        span.id = spanName;
        span.className = "span-intv, card";
        span.innerHTML = spanHTML;
        document.getElementById(divName).appendChild(span); 
        
        /*create btn1 */
        var btn = document.createElement("BUTTON"); 
        btn.innerHTML = "+"; 
        btn.id = node["id"];
        btn.className = "btn btn-warning btn-intervention";
        btn.onclick = function(){
            /* .onclick function POST request to API for intervention */
            var xhr = new XMLHttpRequest();        

            var target = btn.id

            xhr.open("POST", "http://127.0.0.1:5000/intervene", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 201) {
                    console.log(4,201);
                }
                if (xhr.readyState === 4 && xhr.status === 303) {
                    console.log(4,303);
                }
            }
            xhr.send(JSON.stringify({
            "id": target,
            "valence": "+",
            "value": "1"
            }));
        };
        document.getElementById(spanName).appendChild(btn); 
       
        /*create btn2 */
        var btn = document.createElement("BUTTON"); 
        btn.innerHTML = "-"; 
        btn.id = node["id"];
        btn.className = "btn btn-warning btn-intervention";
        btn.onclick = function(){
            /* .onclick function POST request to API for intervention */
            var xhr = new XMLHttpRequest();        

            var target = btn.id

            xhr.open("POST", "http://127.0.0.1:5000/intervene", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 201) {
                    console.log(4,201);
                }
                if (xhr.readyState === 4 && xhr.status === 303) {
                    console.log(4,303);
                }
            }
            xhr.send(JSON.stringify({
            "id": target,
            "valence": "-",
            "value": "1"
            }));
        };
        document.getElementById(spanName).appendChild(btn); 
        
    }
        
};