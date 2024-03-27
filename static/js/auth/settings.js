$(document).ready(function () {
    /*
    let box = document.querySelector('input[id="darkmode_checkbox"]')
    if (box.checked) {
        console.log('check')
    } else {
        console.log('no check')
    }*/
    $('#darkmode_checkbox').change(function (e) { 
        e.preventDefault();
        //console.log(e.target.checked)
        
        $.ajax({
            type: "POST",
            url: "/auth/settings_darkmode_ajax",
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                darkmode_check: e.target.checked,
            },
            success: function (response) {
                if (response.ok === 'success') {
                    window.location.reload()
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

    $('#album_date_sort_checkbox').change(function (e) { 
        e.preventDefault();
        //console.log(e.target.checked)
        
        $.ajax({
            type: "POST",
            url: "/auth/settings_album_date_sort_ajax",
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                album_date_sort_check: e.target.checked,
            },
            success: function (response) {
                if (response.ok === 'success') {
                    console.log('asd')
                    //window.location.reload()
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