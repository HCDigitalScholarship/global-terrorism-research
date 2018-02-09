var checkboxes = {};

$(document).ready(function () {
    for (var i = 0; i < allKeywords.length; i++) {
        checkboxes[allKeywords[i]] = {
            name: allKeywords[i], count: 0, include: false, exclude: false
        };
    }

    var table = $("#mainTable").DataTable({
        columnDefs: [
          {visible: false, targets: [2]}
        ]
    });
    renderKeywords(table);

    // Inspired by stackoverflow.com/questions/30086341
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        for (var key in checkboxes) {
            if (checkboxes.hasOwnProperty(key) && checkboxes[key].include) {
                if (!data[2].includes('|' + key + '|')) {
                    return false;
                }
            }
        }
        for (var key in checkboxes) {
            if (checkboxes.hasOwnProperty(key) && checkboxes[key].exclude) {
                if (data[2].includes('|' + key + '|')) {
                    return false;
                }
            }
        }
        return true;
    });

    $(".include-checkbox").change(makeCallback(table, "include"));
    $(".exclude-checkbox").change(makeCallback(table, "exclude"));
});


function parseKeywordStr(keywordStr) {
    return keywordStr.substring(1, keywordStr.length - 1).split('""');
}


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
    elems.sort(checkboxCmp);
    parentNode.append(elems);
}


function checkboxCmp(checkbox1, checkbox2) {
    var count1 = checkboxCount($(checkbox1));
    var count2 = checkboxCount($(checkbox2));
    return count2 - count1;
}


function checkboxCount(elem) {
    return parseInt(elem.children("span").first().text());
}


// Render the keywords and their counts in the "Include" and "Exclude" columns.
//   This function takes the DataTable object as a parameter, because that is where all the data is
//   ultimately stored.
//
//   Note: This function uses (but does not modify) the global variable `checkboxes`.
function renderKeywords_OLD(table) {
    for (var key in checkboxes) {
        if (checkboxes.hasOwnProperty(key)) {
            checkboxes[key].count = 0;
        }
    }

    // Calculate the count of each keyword.
    table.rows({search: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
        var data = this.data();
        var keywords = data[2].split('|');
        for (var i = 0; i < keywords.length; i++) {
            var keyword = keywords[i];
            if (keyword.length !== 0) {
                if (keyword in checkboxes) {
                    checkboxes[keyword].count++;
                } else {
                    console.log(keyword);
                }
            }
        }
    });

    var includeKeywords = getIncludeKeywords();
    var excludeKeywords = getExcludeKeywords();

    $("#include-buttons").empty();
    $("#exclude-buttons").empty();

    for (var i = 0; i < includeKeywords.length; i++) {
        var item = includeKeywords[i];
        $("#include-buttons").append(makeCheckbox(item, "include"));
    }
    for (var i = 0; i < excludeKeywords.length; i++) {
        var item = excludeKeywords[i];
        $("#exclude-buttons").append(makeCheckbox(item, "exclude"));
    }
}


function makeCallback(table, propertyToUpdate) {
    return function () {
        var name = $(this).attr("name");
        if (this.checked) {
            checkboxes[name][propertyToUpdate] = true;
        } else {
            checkboxes[name][propertyToUpdate] = false;
        }
        table.draw();
        renderKeywords(table);
    };
}


// Return an HTML string for a keyword checkbox, where `type` is either 'exclude' or 'include'.
function makeCheckbox(keywordItem, property) {
      return "<li class=\"list-group-item justify-content-between\">" +
        "<input type=\"checkbox\" name=\"" + keywordItem.name + "\" value=\"key_OFF\"" +
               "class=\"filter_check form-check-input " + property + "-checkbox\"" +
               (keywordItem[property] ? " checked" : "") + ">" +
          "   " + keywordItem.name + "<span class=\"badge badge-default badge-pill\">" + keywordItem.count + "</span>" +
      "</li>";
}


function getIncludeKeywords() {
    var keywordsCopy = Object.values(checkboxes);
    keywordsCopy.sort(makeCompareFunction('include'));
    return keywordsCopy.slice(0, 20);
}


function getExcludeKeywords() {
    var keywordsCopy = Object.values(checkboxes);
    keywordsCopy.sort(makeCompareFunction('exclude'));
    return keywordsCopy.slice(0, 20);
}


// Make a function that compare two checkbox objects on the given property, either 'include' or
//   'exclude'.
function makeCompareFunction(prop) {
    // Compare two checkbox objects. Sort checked boxes first, then sort by count, then by name.
    function cmp(a, b) {
        if (a[prop] && !b[prop]) {
            return -1;
        } else if (!a[prop] && b[prop]) {
            return 1;
        } else {
            if (a.count > b.count) {
                return -1;
            } else if (a.count < b.count) {
                return 1;
            } else {
                if (a.name < b.name) {
                    return -1;
                } else if (a.name > b.name) {
                    return 1;
                } else {
                    return 1;
                }
            }
        }
    }
    return cmp;
}
