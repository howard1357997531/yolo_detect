$(document).ready(function () {
    let dark_mode = document.querySelector('#dark-mode');
    let dark_mode_icon = document.querySelector('#dark-mode-icon');
    let dark_mode_name = document.querySelector('.dark-mode-name');
    let content_wrapper = document.querySelector('#content-wrapper');
    
    let page_link = document.querySelectorAll('.page-links')
    page_link.forEach(el => {
        el.addEventListener('click', () => {
            localStorage.removeItem('page-links')
            localStorage.setItem('page-links', el.id)
        })
    })

    let dropdown_nav = document.querySelectorAll('#dropdown-nav')
    let sidebar_scroll_part = document.querySelector('.scroll-part')

    // document全域事件比普通element事件還晚執行
    document.addEventListener('click', (e) => {
        if (e.target !== $('#sidebar-web-camera-fixed')[0] || e.target !== $('#sidebar-intel-camera-fixed')[0]
            || e.target !== $('#sidebar-camera-split-fixed')[0]) {
            $('#collapseCamera').removeClass('show');
        }
        if (e.target !== $('#sidebar-single-image-fixed')[0] || e.target !== $('#sidebar-multiple-image-fixed')[0]) {
            $('#collapseImage').removeClass('show');
        }
        if (e.target !== $('#sidebar-album-photo-fixed')[0] || e.target !== $('#sidebar-album-video-fixed')[0]) {
            $('#collapseAlbum').removeClass('show');
        }
        if (e.target !== $('#sidebar-folder-multiple-image-fixed')[0]) {
            $('#collapseFolder').removeClass('show');
        }
        if (e.target !== $('.language-en')[0] && e.target !== $('.language-zh')[0]) {
            $('#collapseLanguage').removeClass('show');
        }
    })
    
    dropdown_nav.forEach((el, index) => {
        el.addEventListener('click', () => {
            $('.fixed-inner').removeAttr('style');
            if (window.innerWidth >= 768) {
                if ($('.navbar-nav.sidebar').hasClass('toggled')) {
                    $(`.fixed-inner${index + 1}`).css('top', `${el.getBoundingClientRect().y}px`);
                } else {
                    $(`.fixed-inner${index + 1}`).css('display', 'none');
                }
            } else {
                $(`.fixed-inner${index + 1}`).css('top', `${el.getBoundingClientRect().y}px`);
            }
        })
    })

    sidebar_scroll_part.addEventListener('scroll', () => {
        if(window.innerWidth >= 768) {
            if ($('.navbar-nav.sidebar-color.sidebar.accordion').hasClass('toggled')) {
                $('#collapseCamera, #collapseImage, #collapseAlbum, #collapseLanguage').removeClass('show');
            };
        } else {
            $('#collapseCamera, #collapseImage, #collapseAlbum, #collapseLanguage').removeClass('show');
        }
    })

    dark_mode.addEventListener('click', () => {
        // console.log(dark_mode_icon.classList.toggle('asd)) 若 toggle 值不存在會回傳 True
        if (dark_mode_icon.classList.toggle('fa-light')) {
            localStorage.removeItem('dark_mode')
            dark_mode_icon.classList.toggle('fa-moon')
            dark_mode_icon.classList.toggle('fa-sharp')
            dark_mode_icon.classList.toggle('fa-regular')
            dark_mode_icon.classList.toggle('fa-sun')
            content_wrapper.classList.remove('bg-dark')
            content_wrapper.classList.remove('text-white')

            $('.navbar.navbar-expand.navbar-light').removeClass('nav-dark-shadow');
            $('#content-wrapper .navbar.navbar-expand').removeClass('bg-dark');
            $('html').removeAttr('style')
            $('.user-name-color').removeClass('user-name-color-darkmode');
            $('.photo .datetime, .photo .photo-card p').removeAttr('style');
            $('.scroll-to-top').removeClass('scroll-to-top-darkmode');

            if (localStorage.getItem('language')) {
                dark_mode_name.innerText = '夜間模式'
            } else {
                dark_mode_name.innerText = 'Dark Mode'
            };
            
            if (localStorage.getItem('page-links') === 'sidebar-web-camera' || localStorage.getItem('page-links') === 'sidebar-intel-camera') {
                $('#web-camera-title, #intel-camera-title').removeClass('h1-3D-dark');
                $('#web-camera-loading').removeClass('text-shadow-cum');
                $('.yolo-output').removeClass('border-dark');
                $('.btn-style1').removeClass('btn-style1-dark');
                $('.ratio-detail').removeClass('radio-detail-border-dark');
            } else if (localStorage.getItem('page-links') === 'sidebar-single-image') {
                $('.card1, .second-containe').removeClass('image_card_border_dark');
                $('#image-image1-title').removeClass('h1-3D-dark');
                $('.group-btn .btn-style1').removeClass('btn-style1-dark');
            } else if (localStorage.getItem('page-links') === 'sidebar-multiple-image') {
                $('#image-multiple-title').removeClass('h1-3D-dark');
                $('#my-dropzone').removeClass('border-dark');
            } else if (localStorage.getItem('page-links') === 'video-page') {
                $('#video-title').removeClass('h1-3D-dark');
                $('.yolo-video .card1').removeClass('image_card_border_dark');
                // $('.left-btn, .right-btn').removeClass('btn-style1-dark');
            }  else if (localStorage.getItem('page-links') === 'sidebar-folder-multiple-image') {
                $('.image_multiple_folder .f .folder').css('box-shadow', 'rgba(0, 0, 0, 0.117647) 0px 1px 6px, rgba(0, 0, 0, 0.117647) 0px 1px 4px');
            }  else if (localStorage.getItem('page-links') === 'camera-split-setting') {
                $('.camera-name').removeAttr('style');
            }    
        } else {
            localStorage.setItem('dark_mode', 'dark')
            dark_mode_icon.classList.toggle('fa-moon')
            dark_mode_icon.classList.toggle('fa-sharp')
            dark_mode_icon.classList.toggle('fa-regular')
            dark_mode_icon.classList.toggle('fa-sun')
            content_wrapper.classList.add('bg-dark')
            content_wrapper.classList.add('text-white')

            $('html').css('background-color', '#5a5c69');
            if (localStorage.getItem('page-links') !== 'sidebar-single-image' && localStorage.getItem('page-links') !== 'sidebar-multiple-image'
                && localStorage.getItem('page-links') !== 'video-page') {
                    $('.navbar.navbar-expand.navbar-light').addClass('nav-dark-shadow');
            }
            
            $('.user-name-color').addClass('user-name-color-darkmode');
            $('#content-wrapper .navbar.navbar-expand').addClass('bg-dark');
            $('.photo .datetime, .photo .photo-card p').css('color', 'rgb(255, 169, 20)');
            $('.scroll-to-top').addClass('scroll-to-top-darkmode');
            if (localStorage.getItem('language')) {
                dark_mode_name.innerText = '日間模式'
            } else {
                dark_mode_name.innerText = 'Light Mode'
            };
            
            if (localStorage.getItem('page-links') === 'sidebar-web-camera' || localStorage.getItem('page-links') === 'sidebar-intel-camera') {
                $('#web-camera-title, #intel-camera-title').addClass('h1-3D-dark');
                $('#web-camera-loading').addClass('text-shadow-cum');
                $('.yolo-output').addClass('border-dark');
                $('.btn-style1').addClass('btn-style1-dark');
                $('.ratio-detail').addClass('radio-detail-border-dark');
            } else if (localStorage.getItem('page-links') === 'sidebar-single-image') {
                $('.card1, .second-containe').addClass('image_card_border_dark');
                $('#image-image1-title').addClass('h1-3D-dark');
                $('.group-btn .btn-style1').addClass('btn-style1-dark');
            } else if (localStorage.getItem('page-links') === 'sidebar-multiple-image') {
                $('#image-multiple-title').addClass('h1-3D-dark');
                $('#my-dropzone').addClass('border-dark');
            } else if (localStorage.getItem('page-links') === 'video-page') {
                $('#video-title').addClass('h1-3D-dark');
                $('.yolo-video .card1').addClass('image_card_border_dark');
                // $('.left-btn, .right-btn').addClass('btn-style1-dark');
            } else if (localStorage.getItem('page-links') === 'sidebar-folder-multiple-image') {
                $('.image_multiple_folder .f .folder').css('box-shadow', 'cadetblue 0px 1px 6px, cadetblue 0px 1px 4px');
            } else if (localStorage.getItem('page-links') === 'camera-split-setting') {
                $('.camera-name').css('color', '#fff');
            }
        }       
    })
    
    let accordionSidebar = document.querySelector('#accordionSidebar')
    window.addEventListener('resize', () => {
        if (accordionSidebar.classList.contains('toggled')) {
            if (window.innerWidth >= 768) {
                content_wrapper.classList.remove('left-0rem')
                content_wrapper.classList.add('left-6rem')
            } else if (490 <= window.innerWidth && window.innerWidth < 768) {
                content_wrapper.classList.remove('left-6rem');
                content_wrapper.classList.remove('left-14-6-0rem');
                $(`.fixed-inner`).removeClass('show');
                if (localStorage.getItem('language') == 'zh') {
                    $('.photo .photo-btn-group').css('width','200px');
                }
            } else if (window.innerWidth < 490) {
                content_wrapper.classList.add('left-0rem')
                $(`.fixed-inner`).removeClass('show')
                if (localStorage.getItem('language')) {
                    $('.photo .photo-btn-group').css('width','140px');
                }
            }
        } else { //到底往右拉有問題
            // 一開始螢幕全開(768以上)無toggle,到490下出現toggle，再往回拉toggle不會消失
            // 但如果reload, 在490下toggle會消失，但是一往右resize toggle會出現直到最後
            // 若在490以上reload, 往右resize不會出現toggle
            if (window.innerWidth >= 768) {
                $('#content-wrapper').removeClass('left-6rem').addClass('left-14rem')
                $(`.fixed-inner`).css('display', 'none');
            } else if (490 <= window.innerWidth && window.innerWidth < 768) {
                $('#content-wrapper').removeClass('left-14rem').addClass('left-6rem')
                if (localStorage.getItem('language') == 'zh') {
                    $('.photo .photo-btn-group').css('width','200px');
                }
            } else if (window.innerWidth < 490) {
                if (localStorage.getItem('language') == 'zh') {
                    $('.photo .photo-btn-group').css('width','140px');
                }
            }
        }

        if (window.innerWidth <= 1000) {
            $('.web-camera .wh').removeClass('wh-max');
            $('#web-camera-full-screen-btn').removeClass('active-btn');
            if (localStorage.getItem('language') === 'zh') {
                $('#web-camera-full-screen-btn').text('全螢幕')
            } else {
                $('#web-camera-full-screen-btn').text('Full')
            }
            if ($('.web-camera .wh').hasClass('wh16-9')) {
                $('#16-9btn').addClass('active-btn');
            } else {
                $('#4-3btn').addClass('active-btn');
            }
        }
    })

    // alert 
    let alertMessage = document.querySelectorAll('.alert-message');
    alertMessage.forEach(el => {
        el.addEventListener('click', () => {
            localStorage.setItem('alert', el.getAttribute('data-alert-id'))
        })
    })

    $('#alert-show-all-alert').click(function () { 
        localStorage.removeItem('alert');
    });

    $('.alert_btn').click(function (e) {
        e.preventDefault();
        if ($('.badge.badge-danger.badge-counter').text() !== ''){
            $('.badge.badge-danger.badge-counter').text('');
            $.ajax({
                type: "POST",
                url: "/auth/alert_ajax",
                data: {
                    'csrfmiddlewaretoken': $('.nav-item.dropdown.alertcsrf input[name="csrfmiddlewaretoken"]').val(),
                },
                success: function (response) {
                    if (response.ok === 'success') {
                    }
                },
                error: function (data) {
                    setTimeout(() => {
                        Swal.fire({
                            icon: 'error',
                            title: localStorage.getItem('language') === 'zh'
                                    ? '發生未知錯誤'
                                    : 'An unknown error occurred',
                            color: '#fff',
                            background: 'cadetblue',
                        }).then(() => {
                            window.location.reload()
                        })
                    }, 2000);
                    },
                });
        } else {
            $('.alert-message').removeAttr('style');
            // $('.icon-circle').removeClass('alert-animate');
        }
        
    });
    // --------------------------------

    $('#sidebarToggleTop').click(function () {
        if ($('.navbar-nav.sidebar').hasClass('toggled')) { //關閉
            $('#content-wrapper').removeClass('left-14-6-0rem').addClass('left-0rem')
        } else {
            $('#content-wrapper').removeClass('left-0rem').addClass('left-6rem');
        }
    });

    $('.sidebar-downbtn').click(function () { 
        $('.fixed-inner').removeAttr('style');
        if ($('.navbar-nav.sidebar').hasClass('toggled')) { //關閉
            $('#content-wrapper').removeClass('left-14rem').addClass('left-6rem')
        } else {
            $('#content-wrapper').removeClass('left-6rem').addClass('left-14rem')
        }
    });

    if (location.pathname.slice(7,12) !== 'photo') {
        localStorage.removeItem('photo_url');
        localStorage.removeItem('photo_position');
    } 
    if (location.pathname.slice(7,18) !== 'album_video') {
        localStorage.removeItem('album_video_url');
        localStorage.removeItem('album_video_position');
    }

    alertify.set('notifier','position', 'top-center');
});

// 按提醒系統到圖片，若開啟自動夜間模式，在黑夜的時候過去，文字顏色顯示會有問題

