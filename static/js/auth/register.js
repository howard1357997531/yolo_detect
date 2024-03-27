$(document).ready(function () {
    $('.email').blur(function (e) { 
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
    
    $('.aasd').click(function (e) { 
        e.preventDefault()
        let data =  {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),  
            username: $('input[name="username"]').val(),
            first_name: $('input[name="first_name"]').val(),
            email: $('input[name="email"]').val(),
            password1: $('input[name="password1"]').val(),
            password2: $('input[name="password2"]').val(),
          }
        console.log(data)
        $.ajax({
            type: "POST",
            url: "/auth/register_ajax",
            data: {
              csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),  
              username: $('input[name="username"]').val(),
              first_name: $('input[name="first_name"]').val(),
              email: $('input[name="email"]').val(),
              password1: $('input[name="password1"]').val(),
              password2: $('input[name="password2"]').val(),
            },
            success: function (response) {
              if (response.ok === 'success') {
                console.log(response.a)
              }
            },
            error: function (data) {
                setTimeout(() => {
                    Swal.fire({
                        icon: 'error',
                        title: localStorage.getItem('language') === 'zh'
                                  ? '發生未知錯誤'
                                  : 'An unknown error occurred',
                    }).then(() => {
                        window.location.reload()
                    })
                }, 2000);
            },
          });
        
    });

});