var edgeContainer = document.getElementById("edgeInfo");    
var btn = document.getElementById("btn");
var btnAll = document.getElementById("btnAll");
var btnAllAnnot = document.getElementById("btnAllAnnot");
var btnAnnot = document.getElementById("btnAnnot");

/* Display one edge in sentance */
btn.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET','http://127.0.0.1:5000/edges');
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log((ourData['edges'])[0]);
        renderHTML((ourData['edges'])[0]);
    };
    ourRequest.send(); 
});

function renderHTML(data) {
    var htmlString = "";

    
    htmlString += "<p>Edge sentance:<br>" + "The edge with ref #" + data['ref'] + 
    " models the exposure " + data['exp_name'] + " against the outcome " + data['out_name'] 
    + " and has an MR estimate of " + data['MRestimate'] + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}

/* Display all edges in edges list */
btnAll.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET','http://127.0.0.1:5000/edges');
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData['edges']);
        renderHTML2(ourData['edges']);
    };
    ourRequest.send(); 
});

function renderHTML2(data) {
    var htmlString = "";
    json = JSON.stringify(data, null, 2);
    htmlString += "<p>List of edges:<br>" + json + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}

/* Display one annotation for an edge in sentance */
btnAnnot.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET','http://127.0.0.1:5000/annotations');
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log((ourData['annotations'])[0]);
        renderHTML4((ourData['annotations'])[0]);
    };
    ourRequest.send(); 
});

function renderHTML4(data) {
    var htmlString = "";
    annotations  = "";
    json = JSON.stringify(data);
    annots = data
    htmlString += "<p>Annotation sentance:<br>" + "The edge with ref #" + data['ref'] 
        + " received an annotation from user " + data['username'] + " who made the judgement " + data['judgement'] 
    + " where 0=false and 1=true, with the comment: that " + data['comment'] + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}

/* Display all annotations for edge */
btnAllAnnot.addEventListener("click", function() {
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET','http://127.0.0.1:5000/annotations');
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData['annotations']);
        renderHTML3(ourData['annotations']);
    };
    ourRequest.send(); 
});

function renderHTML3(data) {
    var htmlString = "";
    annotations  = "";
    json = JSON.stringify(data);
    annots = data
    htmlString += "<p>List of annotations:<br>" + json + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}

/* Loop to put all annots in sentence */
    /* for (i = 0; i < annots.length; i++) {
        annotations += JSON.stringify(annots['comment']);
    } */