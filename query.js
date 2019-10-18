window.onload=function(){
 
    var btn_intervention = document.getElementById("btn_intervention");
    var form_intervention = document.getElementById("form_intervention");
    
    /* Retrieve nodes in data */
    var ourRequest = new XMLHttpRequest();
        ourRequest.open('GET', "http://127.0.0.1:5000/simulation");
        ourRequest.onload = function() {
            var ourData = JSON.parse(ourRequest.responseText);
            ourData["nodes"].forEach(renderBtn);
        };
        ourRequest.send();
    
    /* Automatically create buttons for nodes in data */
    count=1
    function renderBtn(node){
        btnName = "btn"+count
        var btn = document.createElement("BUTTON"); 
        btn.innerHTML = node["shortName"]; 
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
            }));
        };
        document.body.appendChild(btn); 
        count ++
    }
        
};