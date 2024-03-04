window.addEventListener('load', function () {
    setTimeout(function () {
        document.querySelector('.loader-container').classList.remove('active');
        $('.loader-container').fadeOut('slow');
    },2000);
})