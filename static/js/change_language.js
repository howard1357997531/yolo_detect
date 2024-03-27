$(document).ready(function () {
    let languageSelect = document.querySelectorAll('.language-select a');
    languageSelect.forEach((el) => {
        el.addEventListener('click', () => {
            if (el.classList.contains('language-en')) {
                localStorage.removeItem('language')
                for (let key in translations['en']) {
                    $(`#${key}`).text(translations['en'][key]);
                }
            } else {
                localStorage.setItem('language', 'zh')
                for (let key in translations['zh']) {
                    $(`#${key}`).text(translations['zh'][key]);
                }
            }
        })
    })

    if (localStorage.getItem('language') === 'zh') {
        for (let key in translations['zh']) {
            $(`#${key}`).text(translations['zh'][key]);
        }
        setTimeout(() => {
            $('#image-multiple-dz-button').text('請拖曳或選擇檔案至此');
        }, 10);
    }

    if (localStorage.getItem('dark_mode')) {
        let dark_mode_icon = document.querySelector('#dark-mode-icon')
        let dark_mode_name = document.querySelector('.dark-mode-name')
        let content_wrapper = document.querySelector('#content-wrapper')
        dark_mode_icon.classList.toggle('fa-moon')
        dark_mode_icon.classList.toggle('fa-sharp')
        dark_mode_icon.classList.toggle('fa-regular')
        dark_mode_icon.classList.toggle('fa-sun')
        content_wrapper.classList.add('bg-dark')
        content_wrapper.classList.add('text-white')

        $('html').css('background-color', '#5a5c69')
        if (localStorage.getItem('page-links') !== 'sidebar-single-image' && localStorage.getItem('page-links') !== 'sidebar-multiple-image'
            && localStorage.getItem('page-links') !== 'video-page') {
            $('.navbar.navbar-expand.navbar-light').addClass('nav-dark-shadow');
        }
        $('.user-name-color').addClass('user-name-color-darkmode');
        $('#dark-mode-icon').removeClass('fa-light');
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
});

let translations = {
    'en': {
    // sidebar
        'sidebar-web-camera-fixed': 'Web Camera',
        'sidebar-intel-camera-fixed': 'Intel Camera',
        'sidebar-single-image-fixed': 'Single Image',
        'sidebar-multiple-image-fixed': 'Multiple Image',
        'sidebar-album-photo-fixed': 'Photo',
        'sidebar-album-video-fixed': 'Video',
        'sidebar-title': 'YOLO',
        'sidebar-dashboard': 'Dashboard',
        'sidebar-tool': 'Tool',
        'sidebar-camera': 'Camera',
        'sidebar-web-camera': 'Web Camera',
        'sidebar-intel-camera': 'Intel Camera',
        'sidebar-image': 'Image',
        'sidebar-single-image': 'Single Image',
        'sidebar-multiple-image': 'Multiple Image',
        'sidebar-video': 'Video',
        'sidebar-public':'Public',
        'sidebar-private':'Private',
        'sidebar-album': 'Album',
        'sidebar-album-photo': 'Photo',
        'sidebar-album-video': 'Video',
        'sidebar-folder': 'Folder',
        'sidebar-folder-multiple-image': 'Multiple Image',
        'sidebar-analyse': 'Analyse',
        'sidebar-setting': 'Setting',
        'sidebar-language': 'Language',
        'sidebar-darkmode': 'Dark Mode',
    // nav
        'nav-guest': 'guest',
        'nav-alertcenter':'Alerts Center',
        'nav-profile': 'Profile',
        'nav-setting': 'Settings',
        'nav-database': 'Database',
        'nav-logout': 'Logout',
        'nav-login': 'Login',
        // alert_show_all
        'alert-show-all-title': 'Notification',
        'alert-show-all-alert': 'Show All Alerts',
        // login
        'login-title': 'Sign in',
        'login-username': 'Username',
        'login-password': 'Password',
        'login-forget-password': 'Forgot Password',
        'login-signup': 'Sign up',
        'login-submitbtn': 'login',
        // register
        'register-title': 'Create Account',
        'register-account-number': 'Account number',
        'register-name': 'Name',
        'register-email': 'Email',
        'register-password': 'Password',
        'register-password-confirm': 'Password Confirm',
        'register-signin': 'Sign in',
        'register-submitbtn': 'Sign Up',
        // profile
        'profile-title': 'Profile Setting',
        'profile-name': 'Name',
        'profile-email': 'Email',
        'profile-image': 'Image',
        'profile-file': 'Choose a Image',
        'profile-submitbtn': 'Send',
        // settings
        'settings-title': 'Settings',
        'settings-text1': 'Advanced Dark mode',
        'settings-subtext1-1': 'After this mode is turned on, it will automatically switch to Light and Dark mode',
        'settings-subtext1-2': 'Light mode start time : 6 a.m.',
        'settings-subtext1-3': 'Dark mode start time : 6 p.m.',
        'settings-text2': 'Album date sorting',
        'settings-subtext2-1': 'After this mode is turned on, date sorting descending',
        'settings-change-password': 'Password Change',
            // password_change_form
            'password-change-title': 'Password Change',
            'password-change-old-password': 'Old Password',
            'password-change-new-password': 'New Password',
            'password-change-new-password-confirm': 'New Password Confirm',
            'password-change-back': 'Back',
            'password-change-submitbtn': 'Send',
            // password_change_done
            "password-change-done-title": 'Success',
            "password-change-done-text": 'New password has been done ~ ~',
            "password-change-done-back": 'Back',
            // password_reset
            "password-reset-title": 'Password Reset',
            // password_reset_done
            "password-reset-done-text1": 'password sent successfully',
            "password-reset-done-text2": 'Please check your email',
            // password_reset_confirm
            "password-reset-confirm-text": 'password has already reset or expired',
            // password_reset_complete
            "password-reset-complete-text": 'New password has been done ! !',
            "password-reset-complete-signin": 'Sign in',
    // camera
        // web camera
        'web-camera-title': 'Web Camera',
        'web-camera-ratio-detail-custom-scale': 'Custom scale : ',
        'web-camera-ratio-detail-sendbtn': 'Send',
        'web-camera-ratio-detail-commonly-used': 'Commonly used :',
        'web-camera-full-screen-btn': 'Full',
        'web-camera-loading': 'loading',
        'web-camera-openbtn': 'Open Camera',
        'web-camera-closebtn': 'Close Camera',
        "camera-change-lg-size": 'widen',
        "camera-change-sm-size": 'small',
        // intel camera
        'intel-camera-title': 'Intel Camera',
    // image
        'image-image1-title': 'Original',
        'image-image1-text1': 'Drap the image here',
        'image-image1-text2': 'Choose a Image',
        'image-image1-left-btn': 'Detect',
        'image-image1-right-btn': 'Back',
        'image-image2-title': 'Output',
        'image-image2-left-btn': 'Download',
        'image-image2-right-btn': 'Back',
        'image-modal': 'loading...',
    //image_multiple
        'image-multiple-title': 'Multiple Image',
        'image-multiple-dz-button': 'Drop or Select files here to upload',
        'image-multiple-openbtn': 'Detect',
        'image-multiple-closebtn': 'Close',
    // video
        'video-title': 'Video',
        'video-text': 'Choose a Video',
        'video-loading': 'loading',
        'video-left-btn': 'Detect',
        'video-right-btn': 'Back',
    // photo
        'photo-title': 'Photo',
        'photo-empty': 'Album is empty',
        'pagination-first': 'First',
        'pagination-last': 'Last',
    // photo_search
        'photo-search-title': 'Photo search',
    // album_video
        'album-video-title': 'Video',
    // album_video_search
        'album-video-search-title': 'Video search',
    // image_multiple_folder
        'image-multiple-folder-title': 'Image multiple folde',
        'image-multiple-folder-empty': 'Folder is empty',
    // image_multiple_folder_search
        'image-multiple-folder-search-title': 'Image multiple folder search',
    }, 
    'zh': {
    // sidebar
        'sidebar-web-camera-fixed': '內建攝影機',
        'sidebar-intel-camera-fixed': 'Intel攝影機',
        'sidebar-single-image-fixed': '單照片輸出',
        'sidebar-multiple-image-fixed': '多照片輸出',
        'sidebar-album-photo-fixed': '圖片',
        'sidebar-album-video-fixed': '影片',
        'sidebar-title': '偵測',
        'sidebar-dashboard': '首頁',
        'sidebar-tool': '工具',
        'sidebar-camera': '相機',
        'sidebar-web-camera': '內建攝影機',
        'sidebar-intel-camera': 'Intel攝影機',
        'sidebar-image': '圖片',
        'sidebar-single-image': '單照片輸出',
        'sidebar-multiple-image': '多照片輸出',
        'sidebar-video': '影片',
        'sidebar-public':'公共',
        'sidebar-private':'私人',
        'sidebar-album': '相簿',
        'sidebar-album-photo': '圖片',
        'sidebar-album-video': '影片',
        'sidebar-folder': '資料夾',
        'sidebar-folder-multiple-image': '多圖片',
        'sidebar-analyse': '分析',
        'sidebar-setting': '設定',
        'sidebar-language': '語言',
        'sidebar-darkmode': '夜間模式',
    // nav
        'nav-guest': '訪客',
        'nav-alertcenter':'通知中心',
        'nav-profile': '個人資料',
        'nav-setting': '設定',
        'nav-database': '資料庫',
        'nav-logout': '登出',
        'nav-login': '登入',
        // alert_show_all
        'alert-show-all-title': '通知',
        'alert-show-all-alert': '顯示所有通知',
        // login
        'login-title': '登入',
        'login-username': '帳號',
        'login-password': '密碼',
        'login-forget-password': '忘記密碼',
        'login-signup': '註冊',
        'login-submitbtn': '送出',
        // register
        'register-title': '建立帳號',
        'register-account-number': '帳號',
        'register-name': '姓名',
        'register-email': '電子郵件',
        'register-password': '密碼',
        'register-password-confirm': '密碼確認',
        'register-signin': '登入',
        'register-submitbtn': '註冊',
        // profile
        'profile-title': '個人資料設定',
        'profile-name': '姓名',
        'profile-email': '電子郵件',
        'profile-image': '大頭照',
        'profile-file': '選擇相片',
        'profile-submitbtn': '送出',
        // settings
        'settings-title': '設定',
        'settings-text1': '日、夜間模式 - 進階',
        'settings-subtext1-1': '此模式開啟之後會自動開關日、夜間模式',
        'settings-subtext1-2': '日間模式開啟時間 : 早上6點',
        'settings-subtext1-3': '夜間模式開啟時間 : 晚上6點',
        'settings-text2': '相簿日期排序(預設:順序)',
        'settings-subtext2-1': '此模式開啟之後日期排序為:倒序',
        'settings-change-password': '修改密碼',
            // password_change_form
            'password-change-title': '密碼修改',
            'password-change-old-password': '舊密碼',
            'password-change-new-password': '新密碼',
            'password-change-new-password-confirm': '新密碼確認',
            'password-change-back': '返回',
            'password-change-submitbtn': '送出',
            // password_change_done
            "password-change-done-title": '密碼重置成功',
            "password-change-done-text": '新密碼已準備好 ~ ~',
            "password-change-done-back": '返回',
            // password_reset
            "password-reset-title": '密碼重置',
            // password_reset_done
            "password-reset-done-text1": '發送重置密碼頁面成功',
            "password-reset-done-text2": '請查看您的電子郵件',
            // password_reset_confirm
            "password-reset-confirm-text": '已重置密碼或過期',
            // password_reset_complete
            "password-reset-complete-text": '新密碼已設置完成 ! !',
            "password-reset-complete-signin": '登入',
    // camera
        // web camera
        'web-camera-title': '內建相機',
        'web-camera-ratio-detail-custom-scale': '自訂比例 : ',
        'web-camera-ratio-detail-sendbtn': '送出',
        'web-camera-ratio-detail-commonly-used': '常用 : ',
        'web-camera-full-screen-btn': '全螢幕',
        'web-camera-loading': '載入中..',
        'web-camera-openbtn': '開啟相機',
        'web-camera-closebtn': '關閉相機',
        "camera-change-lg-size": '大螢幕',
        "camera-change-sm-size": '縮小',
        // intel camera
        'intel-camera-title': 'Intel 相機',
    //image
        'image-image1-title': '輸入',
        'image-image1-text1': '請拖曳檔案至此',
        'image-image1-text2': '選擇相片',
        'image-image1-left-btn': '偵測',
        'image-image1-right-btn': '返回',
        'image-image2-title': '輸出',
        'image-image2-left-btn': '下載',
        'image-image2-right-btn': '返回',
        'image-modal': '載入中...',
    //image_multiple
        'image-multiple-title': '多照片輸出',
        'image-multiple-dz-button': '請拖曳或選擇檔案至此',
        'image-multiple-openbtn': '偵測',
        'image-multiple-closebtn': '關閉',
    // video
        'video-title': '影片',
        'video-text': '選擇影片',
        'video-loading': '載入中..',
        'video-left-btn': '偵測',
        'video-right-btn': '返回',
    // photo
        'photo-title': '圖片',
        'photo-empty': '相簿是空的',
        'pagination-first': '首',
        'pagination-last': '尾',
    // photo_search
        'photo-search-title': '圖片搜尋',
    // album_video
        'album-video-title': '影片',
    // album_video_search
        'album-video-search-title': '影片搜尋',
    // image_multiple_folder
        'image-multiple-folder-title': '多圖片資料夾',
        'image-multiple-folder-empty': '資料夾區是空的',
    // image_multiple_folder_search
        'image-multiple-folder-search-title': '多圖片資料夾搜尋',
    }
}