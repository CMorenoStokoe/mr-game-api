var edgeContainer = document.getElementById("edgeInfo");    
var btn = document.getElementById("btn");
var btnAll = document.getElementById("btnAll");

/* Display one edge */
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

    
    htmlString += "<p>Sentance:<br>" + "The edge with ref #" + data['ref'] + 
    " models the exposure " + data['exp_name'] + " against the outcome " + data['out_name'] 
    + " and has an MR estimate of " + data['MRestimate'] + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}

/* Display first edge in edges list */
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
    json = JSON.stringify(data);
    htmlString += "<p>Sentance:<br>" + "The edge with ref #" + data['ref'] + 
    " models the exposure " + data['exp_name'] + " against the outcome " + data['out_name'] 
    + " and has an MR estimate of " + data['MRestimate'] + "." 
    +"<br><br>Raw:<br>" + json + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}


/* Display annotations for edge */
/*
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
    annotations  = "";
    json = JSON.stringify(data);
    annots = data['annotations']
    for (i = 0; i < annots.length; i++) {
        annotations += JSON.stringify(annots['comment']);
    }
    htmlString += "<p>Sentance:<br>" + "The edge with ref #" + data['ref'] + 
    " models the exposure " + data['exp_name'] + " against the outcome " + data['out_name'] 
    + " and has an MR estimate of " + data['MRestimate'] + "." + annotations
    +"<br><br>Raw:<br>" + json + "</p>";

    edgeContainer.insertAdjacentHTML('beforeend', htmlString);
}
*/