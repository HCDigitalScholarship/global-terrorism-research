// Global variables that hold the names of keywords to be included and excluded.
var include = [];
var exclude = [];

$(document).ready(function () {
    var table = $("#mainTable").DataTable({
        "pageLength": 50,
        "columnDefs": [
          {visible: false, targets: [3]}
        ]
    });
    renderKeywords(table);

    // This function controls which entries are displayed in the table.
    // Inspired by stackoverflow.com/questions/30086341
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        for (var i = 0; i < include.length; i++) {
            if (!data[3].includes('|' + include[i] + '|')) {
                return false;
            }
        }
        for (var i = 0; i < exclude.length; i++) {
            if (data[3].includes('|' + exclude[i] + '|')) {
                return false;
            }
        }
        return true;
    });

    // Each checkbox reorders the checkbox list and filters the table when clicked.
    $(".include-checkbox").change(makeCallback(table, include));
    $(".exclude-checkbox").change(makeCallback(table, exclude));
});


// Update the counts of the keywords and re-sort the keyword lists.
function renderKeywords(table) {
    // Calculate the count of each keyword.
    var counts = {};
    table.rows({search: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
        var data = this.data();
        console.log("Data", data);
        console.log("DATA2", data[3]);
        var keywords = data[3].split('|');
        
        for (var i = 0; i < keywords.length; i++) {
            var keyword = keywords[i];
            if (keyword.length !== 0) {
                if (keyword in counts) {
                    counts[keyword]++;
                } else {
                    console.log("it's zero from this! AND also when we set it below");
                    counts[keyword] = 1;
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
                // This is what has the final say of what the number displayed is
                text = "0";
            }
        }
        $(this).next().text(text);
    });

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


// Return a callback for a checkbox. When the checkbox is checked, its associated keyword is added
// to the `arrayToUpdate` parameter (which should be either the global variable`include` or
// `exclude`), and the keywords and table are re-rendered.
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
