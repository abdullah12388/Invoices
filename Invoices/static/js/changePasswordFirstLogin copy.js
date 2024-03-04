function checkForgetPassword(){
    var password = document.getElementById('new_password');
    var re_password = document.getElementById('re_password');
    var submit_btn = document.getElementById('forgetPasswordBtn');

    if(password.value === re_password.value){
        re_password.classList.remove('bg-danger');
        // console.log('valid');
        submit_btn.type = 'submit';
    }else{
        re_password.classList.add('bg-danger');
        // console.log('not valid');
        submit_btn.type = 'button';
    }
}