$(document).ready(function () {
    var table = $("#mainTable").DataTable({
        columnDefs: [
          {visible: false, targets: [2]}
        ]
    });
    var toInclude = [];
    var toExclude = [];

    /* Inspired by stackoverflow.com/questions/30086341 */
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        var ret = true;
        for (var i = 0; i < toInclude.length; i++) {
            if (!data[2].includes('"' + toInclude[i] + '"')) {
                ret = false;
                break;
            }
        }
        for (var i = 0; i < toExclude.length; i++) {
            if (data[2].includes('"' + toExclude[i] + '"')) {
                ret = false;
                break;
            }
        }
        var keywords = parseKeywordStr(data[2]);
        for (var i = 0; i < keywords.length; i++) {
            if (ret === true) {
                incrementKeyword(keywords[i]);
            } else {
                decrementKeyword(keywords[i]);
            }
        }
        return ret;
    });

    $(".include-checkbox").change(function () {
        var name = $(this).attr("name");
        if (this.checked) {
            toInclude.push(name);
        } else {
            var i = toInclude.indexOf(name);
            toInclude.splice(i, 1);
        }
        resetAllKeywords();
        table.draw();
    });

    $(".exclude-checkbox").change(function () {
        var name = $(this).attr("name");
        if (this.checked) {
            toExclude.push(name);
        } else {
            var i = toExclude.indexOf(name);
            toExclude.splice(i, 1);
        }
        resetAllKeywords();
        table.draw();
    });
});


function parseKeywordStr(keywordStr) {
    return keywordStr.substring(1, keywordStr.length - 1).split('""');
}


function resetAllKeywords() {
    $(".include-checkbox").siblings("span").text("0");
    $(".exclude-checkbox").siblings("span").text("0");
}


function decrementKeyword(name) {
    var includeElem = $(".include-checkbox[name='" + name + "']").siblings("span");
    var excludeElem = $(".exclude-checkbox[name='" + name + "']").siblings("span");
    includeElem.text("" + (parseInt(includeElem.text()) - 1));
    excludeElem.text("" + (parseInt(excludeElem.text()) - 1));
}

function incrementKeyword(name) {
    var includeElem = $(".include-checkbox[name='" + name + "']").siblings("span");
    var excludeElem = $(".exclude-checkbox[name='" + name + "']").siblings("span");
    includeElem.text("" + (parseInt(includeElem.text()) + 1));
    excludeElem.text("" + (parseInt(excludeElem.text()) + 1));
}
