/************************************************
 * Main.js file for gtr_site
 ***********************************************/

$(".ui-autocomplete-multiselect-item").onclick( function () {
    alert("hey);
 });

$.getJSON('/api/v1/keyword/', 
    function(data, textStatus, jqXHR) {
        console.log(data);
    }
)
