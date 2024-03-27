let yolo_output = document.querySelector('.yolo-output');
let camera_openbtn = document.querySelector('#web-camera-openbtn');
let camera_closebtn = document.querySelector('#web-camera-closebtn');
let loading_icon = document.querySelector('.loading-icon');
let loading_text = document.querySelector('.loading-text');
$(document).ready(function () {
    $('.tool-icon').click(function () { 
        if ($('.ratio-detail').css('display') === 'none') {
          $('.ratio-detail').slideDown();
        } else {
          $('.ratio-detail').slideUp();
        }
    });

    $('#web-camera-ratio-detail-sendbtn').click(function () { 
        $('.web-camera #4-3btn, .web-camera #16-9btn, .web-camera #web-camera-full-screen-btn').removeClass('active-btn');
        let width = parseFloat($(".ratio-detail #ratio-detail-width").val())
        let height = parseFloat($(".ratio-detail #ratio-detail-height").val())
        if (width/height > 2) {
            if (localStorage.getItem('language') === 'zh') {
                Swal.fire({
                    icon: 'warning',
                    title: '長度不能超過寬度之2倍',
                  }).then(() => {
                  })
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'The width cannot exceed 2 times than the height',
                  }).then(() => {
                  })
            }
        } else if (height/width > 1.5) {
            if (localStorage.getItem('language') === 'zh') {
                Swal.fire({
                    icon: 'warning',
                    title: '寬度不能超過長度之1.5倍',
                  }).then(() => {
                  })
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'The height cannot exceed 1.5 times than the width',
                  }).then(() => {
                  })
            }
        } else {
            if (window.innerWidth > 1000) {
                if (width >= height) {
                    let h = 40 * (height / width)
                    $('.web-camera .wh').css({'width': '40vw',
                                              'height': `${h}vw`})
                } else if (height > width) {
                    let w = 40 * (width / height)
                    $('.web-camera .wh').css({'width': `${w}vw`,
                                              'height': '40vw'})
                }
            } else if (window.innerWidth <= 1000) {
                if (width >= height) {
                    let h = 72 * (height / width)
                    $('.web-camera .wh').css({'width': '72vw',
                                              'height': `${h}vw`})
                } else if (height > width) {
                    let w = 72 * (width / height)
                    $('.web-camera .wh').css({'width': `${w}vw`,
                                              'height': '72vw'})
                }
            }
        }
        $('.web-camera .wh').removeClass('wh-max');
        if (localStorage.getItem('language') === 'zh') {
            $('#web-camera-full-screen-btn').text('全螢幕');
        } else {
            $('#web-camera-full-screen-btn').text('Full');
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth <= 1000 && window.innerWidth > 990) {
            $('.web-camera .wh').removeAttr('style');
        }
    })

    $('.web-camera .ratio-detail #4-3btn').click(function () { 
        $('.web-camera .wh').removeAttr('style');
        $('.web-camera .wh').removeClass('wh16-9 wh-max wh-top-btn16-9');
        $('.web-camera #16-9btn, .web-camera #web-camera-full-screen-btn').removeClass('active-btn');
        $('.web-camera #4-3btn').addClass('active-btn');
        if (localStorage.getItem('language') === 'zh') {
            $('#web-camera-full-screen-btn').text('全螢幕');
        } else {
            $('#web-camera-full-screen-btn').text('Full');
        }
    });

    $('.web-camera .ratio-detail #16-9btn').click(function () { 
        $('.web-camera .wh').removeAttr('style');
        if ($('.navbar-nav.sidebar').hasClass('toggled') && window.innerWidth <= 560) { //關閉
            $('.web-camera .wh').addClass('wh-top-btn16-9').removeClass('wh-max');
        } else {
            $('.web-camera .wh').addClass('wh16-9').removeClass('wh-max');
        };

        $('.web-camera #4-3btn, .web-camera #web-camera-full-screen-btn').removeClass('active-btn');
        $('.web-camera #16-9btn').addClass('active-btn');
        if (localStorage.getItem('language') === 'zh') {
            $('#web-camera-full-screen-btn').text('全螢幕');
        } else {
            $('#web-camera-full-screen-btn').text('Full');
        }
    });

    $('.web-camera .ratio-detail #web-camera-full-screen-btn').click(function () {
        $('.web-camera .wh').removeAttr('style');
        $('.web-camera #16-9btn, .web-camera #4-3btn').removeClass('active-btn');
        $('.web-camera #web-camera-full-screen-btn').addClass('active-btn');
        let wh_max = document.querySelector('.web-camera .wh')
        if (wh_max.classList.toggle('wh-max')) {
            if (localStorage.getItem('language') === 'zh') {
                $('#web-camera-full-screen-btn').text('縮小');
            } else {
                $('#web-camera-full-screen-btn').text('Small');
            }
        } else {
            if (localStorage.getItem('language') === 'zh') {
                $('#web-camera-full-screen-btn').text('全螢幕');
            } else {
                $('#web-camera-full-screen-btn').text('Full');
            };
            $('.web-camera #web-camera-full-screen-btn').removeClass('active-btn');
            if ($('.web-camera .wh').hasClass('wh16-9')) {
                $('#16-9btn').addClass('active-btn');
            } else {
                $('#4-3btn').addClass('active-btn');
            }
        };
    });

    if (localStorage.getItem('language') === 'zh') {
        $('#ratio-detail-width').attr('placeholder', '長');
        $('#ratio-detail-height').attr('placeholder', '高');
    } else {
        $('#ratio-detail-width').attr('placeholder', 'width');
        $('#ratio-detail-height').attr('placeholder', 'height');
    }

    camera_openbtn.addEventListener('click', () => {
        $('.yolo-output').append(`<img src="/web_camera_video_feed/" alt=""></img>`);
        camera_openbtn.setAttribute('disabled', true);
        camera_closebtn.removeAttribute('disabled')
        loading_icon.style.display = 'block'
        loading_text.style.display = 'block'
    })
    
    camera_closebtn.addEventListener('click', () => {
        yolo_output.innerHTML = ``;
        camera_closebtn.setAttribute('disabled', true);
        window.location.reload();
    })

    let languageSelect = document.querySelectorAll('.language-select a')
    languageSelect.forEach((el) => {
        el.addEventListener('click', () => {
            if (el.classList.contains('language-en')) {
                $('#ratio-detail-width').attr('placeholder', 'width');
                $('#ratio-detail-height').attr('placeholder', 'height');
                if ($('.web-camera .wh').hasClass('wh-max')) {
                    $('#web-camera-full-screen-btn').text('Small');
                }
            } else {
                localStorage.setItem('language', 'zh')
                for (let key in translations['zh']) {
                    $(`#${key}`).text(translations['zh'][key]);
                }
                $('#ratio-detail-width').attr('placeholder', '長');
                $('#ratio-detail-height').attr('placeholder', '高');
                if ($('.web-camera .wh').hasClass('wh-max')) {
                    $('#web-camera-full-screen-btn').text('縮小');
                }
            }
        })
    })

    $('#sidebarToggleTop').click(function () {
        if ($('.navbar-nav.sidebar').hasClass('toggled')) { //關閉
            $('.web-camera .wh').addClass('wh-top-btn');
        } else {
            $('.web-camera .wh').removeClass('wh-top-btn');
        }
    });
});

