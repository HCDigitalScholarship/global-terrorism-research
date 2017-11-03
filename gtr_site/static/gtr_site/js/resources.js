

$(document).ready(function() {
    var table = $("#resourceTable").DataTable({ pageLength: 75 });
    var checked = [];

    /*  Inspired by stackoverflow.com/questions/30086341/  */
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        if (checked.length > 0) {
            return checked.includes(data[3]);
        } else {
            return true;
        }
    });

    function makeCallback(typeString) {
        function checkboxCallback() {
            if (this.checked) {
                checked.push(typeString);
            } else {
                var i = checked.indexOf(typeString);
                checked.splice(i, 1);
                console.log(checked);
            }
            table.draw();
        }
        return checkboxCallback;
    }

    $("#data-source").change(makeCallback("data-source"));
    $("#book").change(makeCallback("book"));
    $("#jihadi-magazines").change(makeCallback("jihadi-magazines"));
    $("#journal-indexes").change(makeCallback("journal-indexes"));
    $("#news").change(makeCallback("news"));
    $("#research").change(makeCallback("research"));
    $("#sites").change(makeCallback("sites"));
    $("#student-resources").change(makeCallback("student-resources"));
    $("#by-country").change(makeCallback("by-country"));
});
