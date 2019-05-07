window.onload=function(){

    var edgeContainer = document.getElementById("edgeInfo");    
    var btnEdge = document.getElementById("btnEdge");
    var btnAllEdge = document.getElementById("btnAllEdge");
    var btnAllAnnot = document.getElementById("btnAllAnnot");
    var btnAnnot = document.getElementById("btnAnnot");
    var btnComm = document.getElementById("btnComm");
    var btnFormUser = document.getElementById("btnFormUser");
    var btnFormComm = document.getElementById("btnFormComm");
    var btnFormUpdComm = document.getElementById("btnFormUpdComm");

    var formExp = document.getElementById("formExp");
    var formOut = document.getElementById("formOut");
    var formComm = document.getElementById("formComm");
    var formUsr = document.getElementById("formUsr");
    var formPass = document.getElementById("formPass");
    var formCommRef = document.getElementById("formCommRef");
    var formCommUsr = document.getElementById("formCommUsr");
    var formCommJudg = document.getElementById("formCommJudg");
    var formDelUser = document.getElementById("formDelUser");
    var formDelExp = document.getElementById("formDelExp");
    var formDelOut = document.getElementById("formDelOut");


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


    /* List all edges 
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


    /* List all annotations 
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
    }*/

    /* Narrate all annotations for one edge */
    btnAnnot.addEventListener("click", function() {
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
        + " where 0=false and 1=true, with the comment: " + data['comment'] + "</p>";

        edgeContainer.insertAdjacentHTML('beforeend', htmlString);
    }


    /*POST new user*/
    btnFormUser.addEventListener("click", function() {
        var xhr = new XMLHttpRequest();
        var usr = formUsr.elements[0].value;
        var pass = formPass.elements[0].value;
        var err = "Error: Username already exists: ";

        xhr.open("POST", "http://127.0.0.1:5000/register", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 201) {
                renderHTML7(usr, pass);
            }
            if (xhr.readyState === 4 && xhr.status === 303) {
                renderHTML7(err, usr);
            };
        };

        xhr.send(JSON.stringify({
        "username": usr,
        "password": pass
        }));
    });

    function renderHTML7(data1, data2) {
        var htmlString = "";
        htmlString += "<p> Registration outcome:" + data1 + data2 + "</p>";

        edgeContainer.insertAdjacentHTML('beforeend', htmlString);
    }

    /*POST comment*/
    btnFormComm.addEventListener("click", function() {
        var xhr = new XMLHttpRequest();
        var ref = formCommRef.elements[0].value;
        var out = formCommOut.elements[0].value;
        var usr = formCommUsr.elements[0].value;
        var comm = formComm.elements[0].value;
        var judg = formCommJudg.elements[0].value;
        var err = "Error: A comment already exists for that edge and username. Please update instead: ";
        var URL = "";
        URL += "http://127.0.0.1:5000/annotations/" + ref + "/" + out;

        var req = JSON.stringify({
            "username": usr,
            "judgement": judg,
            "comment" : comm
        });

        xhr.open("POST", URL , true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 201) {
                renderHTML8(ref, out, usr, judg, comm);
            }
            if (xhr.readyState === 4 && xhr.status === 303) {
                 edgeContainer.insertAdjacentHTML('beforeend', "User has already made a comment for this edge, please update instead.");
            }
        };

        xhr.send(req);
    });

    function renderHTML8(data1, data5, data2, data3, data4) {
        var htmlString = "";
        htmlString += "<p> Annotation made for edge " + data1 + ", " + data5 + " from user " + data2 + " with judgement " + data3 + " and has content: " + data4 + "</p>";

        edgeContainer.insertAdjacentHTML('beforeend', htmlString);
    }

    /*PUT comment*/
    btnFormUpdComm.addEventListener("click", function() {
        var xhr = new XMLHttpRequest();
        var ref = formCommRef.elements[0].value;
        var out = formCommOut.elements[0].value;
        var usr = formCommUsr.elements[0].value;
        var comm = formComm.elements[0].value;
        var judg = formCommJudg.elements[0].value;

        var URL = "";
        URL += "http://127.0.0.1:5000/annotations/" + ref + "/" + out;

        var req = JSON.stringify({
            "username": usr,
            "judgement": judg,
            "comment" : comm
        });

        console.log(req);

        xhr.open("PUT", URL , true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 201) {
                var resp = xhr.responseText;
                console.log(resp);
                renderHTML18(ref, out, usr, comm, judg);
            }
        };

        xhr.send(req);
    });

    function renderHTML18(ref, out, usr, comm, judg) {
        var htmlString = "";
        console.log(htmlString);
        htmlString += "<p> Annotation updated for edge " +  ref + ", " + out + " from user " + usr + " with judgement " + judg + " and has content: " + comm + "</p>";

        edgeContainer.insertAdjacentHTML('beforeend', htmlString);
    }

    /* DELETE edge */
    btnFormDel.addEventListener("click", function() {
        var ourRequest = new XMLHttpRequest();
        var user = formDelUser.elements[0].value;
        var exp = formDelExp.elements[0].value;
        var out = formDelOut.elements[0].value;
        var URL = "";

        URL += "http://127.0.0.1:5000/annotations/del/" + exp + "/" + out + "/" + user;

        ourRequest.open('DELETE', URL);
        ourRequest.onload = function() {
            var ourData = JSON.parse(ourRequest.responseText);
            console.log(ourData);
            renderHTML13(ourData);
        }

        ourRequest.send(); 
    });

    function renderHTML13(data) {
        var htmlString = "";
        annot = data;
        annotations  = "";
        json = JSON.stringify(data);
        htmlString += "<p> Annotation by user " + annot['username'] + " with the judgement " + annot['judgement'] + " and comment " + annot['comment'] + " was deleted. </p>";

        edgeContainer.insertAdjacentHTML('beforeend', htmlString);
    }
};