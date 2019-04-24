var edgeContainer = document.getElementById("edgeInfo");    
var btnEdge = document.getElementById("btnEdge");
var btnAllEdge = document.getElementById("btnAllEdge");
var btnAllAnnot = document.getElementById("btnAllAnnot");
var btnAnnot = document.getElementById("btnAnnot");

var formExp = document.getElementById("formExp");
var formOut = document.getElementById("formOut");
var formComm = document.getElementById("formComm");


/* Narrate multiple edges */
btnEdge.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    var dictKey = "edges";
    var kwrd = "";
    var kwrd2 = "";
    var URL = "";
    
    if (formExp.elements[0].value != "ALL") {
        kwrd += "/" + formExp.elements[0].value;
    };
    if (formOut.elements[0].value != "") {
        kwrd2 += "/" + formOut.elements[0].value;
    
    };
    URL += "http://127.0.0.1:5000/edges" + kwrd + kwrd2;
    
    console.log(dictKey);
    console.log(kwrd);
    console.log(kwrd2);
    console.log(formExp.elements[0].value);
    console.log(URL);
    
    ourRequest.open('GET', URL);
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData["edges"]);
        if (kwrd2 != "") {
            renderHTML(ourData["edges"]);
        }
        else {
            ourData[dictKey].forEach(renderHTML);
        }
        
        
    };
    ourRequest.send(); 
});

function renderHTML(data) {
    var htmlString = "";
    htmlString += "<p>" + "The edge with ref #" + data['ref'] + 
    " models the exposure " + data['exp_name'] + " against the outcome " + data['out_name'] 
    + " and has an MR estimate of " + data['MRestimate'] + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}


/* List all edges */
btnAllEdge.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET','http://127.0.0.1:5000/edges');
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData['edges']);
        ourData['edges'].forEach(renderHTML2);
    };
    ourRequest.send(); 
});

function renderHTML2(data) {
    var htmlString = "";
    json = JSON.stringify(data, null, 2);
    htmlString += "<p>" + json + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}


/* List all annotations */
btnAllAnnot.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET','http://127.0.0.1:5000/annotations');
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData['annotations']);
        ourData['annotations'].forEach(renderHTML3);
    };
    ourRequest.send(); 
});

function renderHTML3(data) {
    var htmlString = "";
    annotations  = "";
    json = JSON.stringify(data);
    annots = data
    htmlString += "<p>" + json + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}


/* Narrate all annotations for one edge */
btnLoopyAnnot.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    
    var kwrd = "";
    var dictKey = "";
    kwrd += "http://127.0.0.1:5000/annotations/" + formExp.elements[0].value;
    dictKey += formExp.elements[0].value;
    
    if (formExp.elements[0].value == "ALL") {
        kwrd = "http://127.0.0.1:5000/annotations";
        dictKey = "annotations";
    };
    
    ourRequest.open('GET', kwrd);
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData);
        console.log(ourData[dictKey]);
        ourData[dictKey].forEach(renderHTML5);
    };
    ourRequest.send(); 
});

function renderHTML5(data) {
    var htmlString = "";
    htmlString += "<p>" + "The edge with ref #" + data['ref'] 
        + " received an annotation from user " + data['username'] + " who made the judgement " + data['judgement'] 
    + " where 0=false and 1=true, with the comment: that " + data['comment'] + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}


/*POST, PUT, DEL REQUESTS*/

/* Post new user 
btnFormUser.addEventListener("click", function() {
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/register";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            console.log(json.username + ", " + json.password);
        }
    };
    var formTxtUser = JSON.stringify({"username": "test196", "password": "pass123"});
    console.log(formTxtUser);
    renderHTML6(formTxtUser);
    xhr.send(formTxtUser);
})

function renderHTML6(data) {
    var htmlString = "";
    annotations  = "";
    json = data;
    annots = data;
    htmlString += "<p>" + "Summary text here; username:" + data['username'] + ", password:" + data['password'] + "; indicates that the request was performed. Check console to see status, 400 returns when User Already Exists." + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}
*/