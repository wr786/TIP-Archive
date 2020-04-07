var tds = [];
var SIZE = 15;
tds.push("<div class='row'>")
for(var i = 0; i < 1; i++) {
    for(var j = 0; j < SIZE; j++) {
        tds.push("<div class='cell' onclick='placeChess(this)' id='c_" + i + "_" + j + "' x='" + i + "' y='" + j + "'><div id='c"+i+j+"' x='" + i + "' y='" + j + "'></div></div>");
    }
}
tds.push("</div>")
for(var i = 1; i < SIZE; i++) {
    tds.push("<div class='row'>");
    for(var j = 0; j < SIZE; j++) {
        tds.push("<div class='cell' onclick='placeChess(this)' id='c_" + i + "_" + j + "' x='" + i + "' y='" + j + "'><div id='c"+i+j+"' x='" + i + "' y='" + j + "'></div></div>");
    }
    tds.push("</div>")
}
$('#grid').html(tds.join(''));