$(function () {
    $("#configurationSearch").on("keyup", function () {
        var searchTerm = $(this).val().toLowerCase();
        $("#configurationResultContainer > button").filter(function () {
            var divText = $(this).text().toLowerCase();
            var isMatch = divText.indexOf(searchTerm) > -1;
            $(this).toggle(isMatch);
            return isMatch;
        });
    });
    // $("#currencySearch").on("keyup", function () {
    //     var searchTerm = $(this).val().toLowerCase();
    //     $("#currencyResultContainer > button").filter(function () {
    //         var divText = $(this).text().toLowerCase();
    //         var isMatch = divText.indexOf(searchTerm) > -1;
    //         $(this).toggle(isMatch);
    //         return isMatch;
    //     });
    // });
    // $("#uomSearch").on("keyup", function () {
    //     var searchTerm = $(this).val().toLowerCase();
    //     $("#uomResultContainer > button").filter(function () {
    //         var divText = $(this).text().toLowerCase();
    //         var isMatch = divText.indexOf(searchTerm) > -1;
    //         $(this).toggle(isMatch);
    //         return isMatch;
    //     });
    // });
    // $("#categorySearch").on("keyup", function () {
    //     var searchTerm = $(this).val().toLowerCase();
    //     $("#categoryResultContainer > button").filter(function () {
    //         var divText = $(this).text().toLowerCase();
    //         var isMatch = divText.indexOf(searchTerm) > -1;
    //         $(this).toggle(isMatch);
    //         return isMatch;
    //     });
    // });
});