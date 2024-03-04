$(function () {
    $("#vendorSearch").on("keyup", function () {
        var searchTerm = $(this).val().toLowerCase();
        $("#vendorResultContainer > button").filter(function () {
            var divText = $(this).text().toLowerCase();
            var isMatch = divText.indexOf(searchTerm) > -1;
            $(this).toggle(isMatch);
            return isMatch;
        });
    });
});