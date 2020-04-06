var tds = [];
tds.push("<tr>")
for(var i = 0; i < 1; i++) {
    for(var j = 0; j < 15; j++) {
        tds.push("<th class='cell' id='c_" + i + "_" + j + "'onclick='placeChess(this)' x='" + i + "' y='" + j + "'>&nbsp;</th>");
    }
}
tds.push("</tr>")
for(var i = 1; i < 15; i++) {
    tds.push("<tr class='row'>");
    for(var j = 0; j < 15; j++) {
        tds.push("<td class='cell' id='c_" + i + "_" + j + "'onclick='placeChess(this)' x='" + i + "' y='" + j + "'>&nbsp;</td>");
    }
    tds.push("</tr>")
}
$('#grid').html(tds.join(''));