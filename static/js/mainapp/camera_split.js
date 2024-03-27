$(document).ready(function () {
    $('.fa-sync-alt').click(function (e) { 
        e.preventDefault();
        window.location.reload();
    });

    let topCamera = document.querySelectorAll('.top-camera');
    topCamera.forEach(el => {
        el.addEventListener('click', () => {
            if ((window.innerWidth > 950 && window.innerHeight > 900) ||
                (window.innerWidth > 660 && window.innerHeight < 750) ) {
                $('.camera').addClass('d-none');
                el.classList.remove('d-none');
                el.classList.add('all-screen');
                $('.camera-split-btn').removeClass('d-none');
            }
        })
    })

    let downCamera = document.querySelectorAll('.down-camera');
    downCamera.forEach(el => {
        el.addEventListener('click', () => {
            if ((window.innerWidth > 950 && window.innerHeight > 900) ||
                (window.innerWidth > 660 && window.innerHeight < 750) ) {
                $('.top-container').css({'position': 'absolute'});
                $('.camera').addClass('d-none');
                el.classList.remove('d-none');
                el.classList.add('all-screen');
                $('.camera-split-btn').removeClass('d-none');
            }
            
        })
    })

    $('.camera-split-btn').click(function (e) { 
        e.preventDefault();
        $('.top-container').removeAttr('style');
        $('.camera').removeClass('d-none all-screen');
        $('.camera-split-btn').addClass('d-none');
    });

    // 不知為何不能用全域，用了上面的addEvent會失效
    // document.addEventListener('click', (e)=>{
    //     if (e.target !== $('.top-container')[0]) {
    //         $('.camera').removeClass('d-none all-screen');
    //     }
    // })

    // nav
    $('.camera-split-setting-btn').click(function () { 
        localStorage.removeItem('page-links');
        localStorage.setItem('page-links', 'camera-split-setting');
    });

    if (localStorage.getItem('language') === 'zh') {
        $('#ratio-detail-width').attr('placeholder', '長');
        $('#ratio-detail-height').attr('placeholder', '高');
    } else {
        $('#ratio-detail-width').attr('placeholder', 'width');
        $('#ratio-detail-height').attr('placeholder', 'height');
    }

    let languageSelect = document.querySelectorAll('.language-select a')
    languageSelect.forEach((el) => {
        el.addEventListener('click', () => {
            if (el.classList.contains('language-en')) {
            } else {

            }
        })
    })

});

