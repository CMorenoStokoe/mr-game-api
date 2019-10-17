window.onload=function(){

    var info_intervention = document.getElementById("info_intervention");   
    var btn_intervention = document.getElementById("btn_intervention");
    var form_intervention = document.getElementById("form_intervention");

    /* Intervention query to API */

    /*POST new user*/
    btn_intervention.addEventListener("click", function() {
        var xhr = new XMLHttpRequest();        
        
        var URL = "";
        var target = form_intervention.elements[0].value                              
        URL += "http://127.0.0.1:5000/intervene/" + target;

        xhr.open("POST", URL, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 201) {
                renderHTML(target);
            }
            if (xhr.readyState === 4 && xhr.status === 303) {
                renderHTML(target);
            }
        
        }
        xhr.send(JSON.stringify({
        "target": target,
        }));
    });

    function renderHTML(target) {
        var htmlString = "";
        htmlString += "<p> Registration outcome:" + target + "</p>";
        info_intervention.insertAdjacentHTML('beforeend', htmlString);
    }

};