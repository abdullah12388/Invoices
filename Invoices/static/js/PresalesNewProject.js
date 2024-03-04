$(function () {
    $("#projectSearch").on("keyup", function () {
        var searchTerm = $(this).val().toLowerCase();
        $("#projectResultContainer > button").filter(function () {
            var divText = $(this).text().toLowerCase();
            var isMatch = divText.indexOf(searchTerm) > -1;
            $(this).toggle(isMatch);
            return isMatch;
        });
    });
});