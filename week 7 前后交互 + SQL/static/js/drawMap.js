var tds = [];
for(var i = 0; i < 15; i++) {
    tds.push("<div class='row'>");
    for(var j = 0; j < 15; j++) {
        tds.push("<div class='cell' id='c_" + i + "_" + j + "'></div>");
    }
    tds.push("</div>")
    $('#grid').html(tds.join(''));
}