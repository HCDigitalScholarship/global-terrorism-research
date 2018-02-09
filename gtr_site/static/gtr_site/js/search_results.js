// Global variables that hold the names of keywords to be included and excluded.
var include = [];
var exclude = [];

$(document).ready(function () {
    var table = $("#mainTable").DataTable({
        "pageLength": 50,
        "columnDefs": [
          {visible: false, targets: [2]}
        ]
    });
    renderKeywords(table);

    // Inspired by stackoverflow.com/questions/30086341
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        for (var i = 0; i < include.length; i++) {
            if (!data[2].includes('|' + include[i] + '|')) {
                return false;
            }
        }
        for (var i = 0; i < exclude.length; i++) {
            if (data[2].includes('|' + exclude[i] + '|')) {
                return false;
            }
        }
        return true;
    });

    $(".include-checkbox").change(makeCallback(table, include));
    $(".exclude-checkbox").change(makeCallback(table, exclude));
});


function renderKeywords(table) {
    // Calculate the count of each keyword.
    var counts = {};
    table.rows({search: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
        var data = this.data();
        var keywords = data[2].split('|');
        for (var i = 0; i < keywords.length; i++) {
            var keyword = keywords[i];
            if (keyword.length !== 0) {
                if (keyword in counts) {
                    counts[keyword]++;
                } else {
                    counts[keyword] = 0;
                }
            }
        }
    });

    // Set the text of the each input's sibling badge to be the keyword's count.
    $("input.filter_check").each(function () {
        var name = $(this).attr("name");
        var text = "";
        if (name in counts) {
            text = "" + counts[name];
        } else {
            if (this.checked && $(this).hasClass("exclude-checkbox")) {
                text = "x";
            } else {
                text = "0";
            }
        }
        $(this).next().text(text);
    });

    // Sort the keywords.
    sortChildren($("#include-buttons"));
    sortChildren($("#exclude-buttons"));
}


function sortChildren(parentNode) {
    var elems = parentNode.children().detach();
    elems.sort(listItemCmp);
    parentNode.append(elems);
}


function listItemCmp(li1, li2) {
    var checked1 = $(li1).children("input").prop("checked");
    var checked2 = $(li2).children("input").prop("checked");
    if (checked1 !== checked2) {
        return (checked1) ? -1 : 1;
    } else {
        var count1 = checkboxCount($(li1));
        var count2 = checkboxCount($(li2));
        return count2 - count1;
    }
}


function checkboxCount(elem) {
    return parseInt(elem.children("span").first().text());
}


function makeCallback(table, arrayToUpdate) {
    return function () {
        var name = $(this).attr("name");
        if (this.checked) {
            arrayToUpdate.push(name);
        } else {
            var i = arrayToUpdate.indexOf(name);
            arrayToUpdate.splice(i, 1);
        }
        table.draw();
        renderKeywords(table);
    };
}
