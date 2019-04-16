var edgeContainer = document.getElementById("edgeInfo");    
var btnEdge = document.getElementById("btnEdge");
var btnAllEdge = document.getElementById("btnAllEdge");
var btnAllAnnot = document.getElementById("btnAllAnnot");
var btnAnnot = document.getElementById("btnAnnot");

/* Narrate one edge */
btnEdge.addEventListener("click", function() {
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
    htmlString += "<p>Edge sentence:<br>" + "The edge with ref #" + data['ref'] + 
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

/* Narrate one annotation for an edge */
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
    htmlString += "<p>Annotation sentence:<br>" + "The edge with ref #" + data['ref'] 
        + " received an annotation from user " + data['username'] + " who made the judgement " + data['judgement'] 
    + " where 0=false and 1=true, with the comment: that " + data['comment'] + "</p>";

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
    ourRequest.open('GET','http://127.0.0.1:5000/annotations/Adiponectin');
    ourRequest.onload = function() {
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData['Adiponectin']);
        ourData['Adiponectin'].forEach(renderHTML5);
    };
    ourRequest.send(); 
});

function renderHTML5(data) {
    var htmlString = "";
    annotations  = "";
    json = JSON.stringify(data);
    annots = data
    htmlString += "<p>" + "The edge with ref #" + data['ref'] 
        + " received an annotation from user " + data['username'] + " who made the judgement " + data['judgement'] 
    + " where 0=false and 1=true, with the comment: that " + data['comment'] + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}


/* Loop to put all annots in sentence */
    /* for (i = 0; i < annots.length; i++) {
        annotations += JSON.stringify(annots['comment']);
    } */