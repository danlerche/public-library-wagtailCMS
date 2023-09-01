$('#searchRadio input').on('change', function() {
var checkbox_value = $('input[name="altSearch"]:checked').val();
if (checkbox_value == 'website') {
$("form#searchForm").attr("action", "/search");
$("input#altSearchInput").attr("name", "query");
}
else {
$("form#searchForm").attr("action", "https://search.pentictonlibrary.ca/Union/Search");
$("input#altSearchInput").attr("name", "lookfor");
}
});
