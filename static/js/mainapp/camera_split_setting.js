$(document).ready(function () {
    $('.fa-sync-alt, .modal-close-btn').click(function (e) { 
        e.preventDefault();
        window.location.reload();
    });

    $('.web-camera-btn').click(function () { 
        $('.web-camera').prepend(
            `<img src="/web_camera_video_feed/" id="image"></img>
            <script>
                const image = document.getElementById('image');
                var cropper = new Cropper(image, {
                    aspectRatio: 4 / 3,
                    viewMode: 1,        //1 mode : restrict the crop box not to exceed the size of the canvas.
                    zoomable: false,    //圖片不可以放大
                    autoCropArea: 0.6,  //裁切範圍
                });
            </script>
            `)
    });

    $('.intel-camera-btn').click(function () { 
        $('.intel-camera').prepend(
            `<img src="/intel_camera_video_feed/" id="image2"></img>
            <script>
                const image2 = document.getElementById('image2');
                var cropper2 = new Cropper(image2, {
                    aspectRatio: 4 / 3,
                    viewMode: 1,        //1 mode : restrict the crop box not to exceed the size of the canvas.
                    zoomable: false,    //圖片不可以放大
                    autoCropArea: 0.6,  //裁切範圍
                });
            </script>
            `) 
    });

    var xCoordinate = 0;
    var yCoordinate = 0;
    var cropBoxWidth = 0;
    var cropBoxHeight = 0;
    var imgWidth = 0;
    var imgHeight = 0;

    $('.modal-crop-btn').hover(function () {
            $('.modal-crop-btn').removeClass('item_animation');
        }, function () {
            // out
        }
    );

    $(".web-camera-crop-btn").on("click", function () {
        let cropperImage = cropper.getCroppedCanvas().toDataURL('image/png');
        document.getElementById('web-camera-output').src = cropperImage;

        let cropData = cropper.getCropBoxData();
        let containerData = cropper.getCanvasData();
 
        xCoordinate = cropData.left;      // 矩形左上角 X 軸座標
        yCoordinate = cropData.top;       // 矩形左上角 Y 軸座標
        cropBoxWidth = cropData.width;    // cropBox 寬度
        cropBoxHeight = cropData.height;  // cropBox 高度
        imgWidth = containerData.width;   // img 寬度
        imgHeight = containerData.height; // img 高度
    });

    $(".intel-camera-crop-btn").on("click", function () {
        let cropperImage2 = cropper2.getCroppedCanvas().toDataURL('image/png');
        document.getElementById('intel-camera-output').src = cropperImage2;

        let cropData = cropper2.getCropBoxData();
        let containerData = cropper2.getCanvasData();
 
        xCoordinate = cropData.left;      // X 軸座標
        yCoordinate = cropData.top;       // Y 軸座標
        cropBoxWidth = cropData.width;    // cropBox 寬度
        cropBoxHeight = cropData.height;  // cropBox 高度
        imgWidth = containerData.width;   // img 寬度
        imgHeight = containerData.height; // img 高度
    });

    $('.original-btn').click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/camera_split_setting_ajax",
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                cameraName: $(this).data('camera'),
                status: 'normal',
            },
            success: function (response) {
                if (response.ok == 'success') {
                    Swal.fire({
                        icon: 'success',
                        color: '#fff',
                        background: 'cadetblue',
                        title: localStorage.getItem('language') === 'zh' ? '儲存成功' : 'success',
                      }).then(() => {
                        window.location.reload();
                      })
                }
            },
            error: function (data) {
                setTimeout(() => {
                  Swal.fire({
                    icon: 'error',
                    color: '#fff',
                    background: 'cadetblue',
                    title: localStorage.getItem('language') === 'zh' ? '發生未知錯誤' : 'An unknown error occurred',
                  }).then(() => {
                    window.location.reload();
                  })
                }, 2000);
              },
        });
    });

    $('.save-btn').click(function (e) { 
        e.preventDefault();
        if (xCoordinate === 0 && yCoordinate === 0 && cropBoxWidth === 0 &&
            cropBoxHeight === 0 && imgWidth === 0 && imgHeight === 0 ) {
            Swal.fire({
                icon: 'warning',
                color: '#fff',
                background: 'cadetblue',
                title: localStorage.getItem('language') === 'zh' ? '尚未進行裁切' : 'Not cropped yet !',
                }).then(() => {
                    $('.modal-crop-btn').addClass('item_animation');
                })
        } else {
            $.ajax({
            type: "POST",
            url: "/camera_split_setting_ajax",
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                cameraName: $(this).data('camera'),
                status: 'split',
                xCoordinate: xCoordinate,
                yCoordinate: yCoordinate,    
                cropBoxWidth: cropBoxWidth, 
                cropBoxHeight: cropBoxHeight,  
                imgWidth: imgWidth,  
                imgHeight: imgHeight,
            },
            success: function (response) {
                if (response.ok == 'success') {
                    if (response.ok == 'success') {
                        Swal.fire({
                            icon: 'success',
                            color: '#fff',
                            background: 'cadetblue',
                            title: localStorage.getItem('language') === 'zh' ? '儲存成功' : 'success',
                          }).then(() => {
                            window.location.reload();
                          })
                    }
                }
            },
            error: function (data) {
                setTimeout(() => {
                  Swal.fire({
                    icon: 'error',
                    color: '#fff',
                    background: 'cadetblue',
                    title: localStorage.getItem('language') === 'zh' ? '發生未知錯誤' : 'An unknown error occurred',
                  }).then(() => {
                    window.location.reload()
                  })
                }, 2000);
              },
        });
        }
    });

    // nav
    $('.camera-split-setting-back-btn').click(function () { 
        localStorage.removeItem('page-links');
        localStorage.setItem('page-links', 'sidebar-camera-split');
    });

    if (localStorage.getItem('language') === 'zh') {
    } else {
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

