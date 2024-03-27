$(document).ready(function () {
    $('#id_email').blur(function (e) { 
        e.preventDefault();
        if (e.target.value) {
            $('.email-i').css('height', '44px');
            $('.email-span').css({'font-size': '0.75em',
                                  'transform': 'translateY(-30px)'});
        } else{
            $('.email-i').removeAttr('style');
            $('.email-span').removeAttr('style');
        }
    });

    $('#profile-file').click(function (e) { 
        e.preventDefault();
        $('#id_image').trigger('click');
    });

    let upload_file = document.querySelector('#id_image');
    upload_file.addEventListener('change', ()=>{
        console.log(upload_file.files[0])
        let reader = new FileReader();
        reader.addEventListener('load', ()=>{
            $('.profile-img').attr('src', reader.result);
        })
        reader.readAsDataURL(upload_file.files[0])
    })

    let upload = document.querySelector('.upload')
    if (upload.children.length > 2) {
        $('#profile-submitbtn').css('margin-top', '80px');
    } else {
        $('#profile-submitbtn').removeAttr('style')
    }
   
    
});