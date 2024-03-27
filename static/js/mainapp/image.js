$(document).ready(function () {
    let body = document.getElementsByTagName('body')[0];
    let uploadFile = document.querySelector('#file');
    let dropContainer = document.querySelector('.first-container');
    let groupBtn_lefttBtn = document.querySelector('.group-btn .left-btn');
    let groupBtn_rightBtn = document.querySelector('.group-btn .right-btn');
    let groupBtn2_leftBtn = document.querySelector('.group-btn2 .left-btn');
    let groupBtn2_rightBtn = document.querySelector('.group-btn2 .right-btn');
    
    //groupBtn_rightBtn
    uploadFile.addEventListener('change', () => {
        console.log(uploadFile.files)
        // console.log(uploadFile.files[0].name)
        if (uploadFile.files[0]) {
            loadImage(uploadFile.files[0])
            switchCard(1);
            $('.group-btn').css('opacity', 1);
            $('.left-btn').removeAttr('disabled');
            $('.right-btn').removeAttr('disabled');
        } else {
            switchCard(0);
        }
        
    })

    body.ondragover = body.ondragend = body.ondrop = () => {
        return false;
    }
    
    dropContainer.addEventListener('drop', (e)=>{
        e.preventDefault();
        loadImage(e.dataTransfer.files[0]);
        switchCard(1);
        $('.group-btn').css('opacity', 1);
        $('.left-btn').removeAttr('disabled');
        $('.right-btn').removeAttr('disabled');
    });

    // let a = document.querySelectorAll('.alert-message');
    // console.log(a[0].children[0].getAttribute('data-item'))
    
    var file_name = ''
    groupBtn_lefttBtn.onclick = (e) => {
        e.preventDefault();
        file_name = uploadFile.files[0].name
        $('#staticBackdrop').modal('show')
        // 不知為何用 formData 會失敗
        let formData = new FormData()
        formData.append('base64', $('.img-card').attr('src'))
        formData.append('file_name', uploadFile.files[0].name)

        // 若使用django ajax post 在url.py ex: path('image_detect', ..)  image_detect後面不能加/
        $.ajax({
            url: "/image_detect",
            type: "POST",
            data: {
                base64: $('.img-card').attr('src'),
                file_name: uploadFile.files[0].name
            },
            // cache: false,      // django ajax post 不能加這些  
            // processData: false,  
            // contentType: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            },
            success: function (response) {
                if (response.ok === 'success') {
                    $('#staticBackdrop').modal('hide')
                    $("#output_image").attr("src", response.base64);
                    $(".card2-img").removeClass('d-none');
                    $('.group-btn').css('opacity', 0);
                    $('.group-btn .left-btn').attr('disabled', true);
                    $('.group-btn .right-btn').attr('disabled', true);
                    $('.group-btn2').css('opacity', 1);
                    let image_image2_title = document.querySelector('#image-image2-title')
                    window.scrollTo({
                        top: image_image2_title.getBoundingClientRect().y,
                        behavior: 'smooth'
                    });
                    
                    let date = new Date();
                    let month_0 = date.getMonth() < 9 ? '0' + String(date.getMonth()+1) : String(date.getMonth()+1);
                    let date_0 = date.getDate() < 10 ? '0' + String(date.getDate()) : String(date.getDate());
                    let minute_0 = date.getMinutes() < 10 ? '0' + String(date.getMinutes()) : String(date.getMinutes());
                    let dateString = `${date.getFullYear()} / ${month_0} / ${date_0}`;

                    if ($('.badge.badge-danger.badge-counter').text() === '') {
                        let alertMessage = document.querySelectorAll('.alert-message');
                        alertMessage.forEach((el, index) => {
                            el.classList.remove(`alert${index + 1}`);
                            el.classList.add(`alert${index + 2}`)
                            el.setAttribute('data-alert-id', `alert${index+2}`);                        
                        });

                        $('#nav-alertcenter').remove();
                        $('.alert-dropdown').prepend(`
                        <a class="dropdown-item d-flex align-items-center alert-message alert1" data-alert-id="alert1" 
                        href="/auth/alert_show_all/" style="background-color: var(--sidebar-inside-color-op0-4)">     
                         <div class="icon-circle alert-icon" style="background-color: var(--bg-1)"
                          data-item="image">
                             <i class="fas fa-solid fa-image text-white"></i>
                         </div>  
                         <div style="margin-left: 55px;">
                             <div style="color: #222 !important; font-size: 13px;">
                                 <span class="alert-date" style="margin-right: 55px;">${dateString}</span>
                                 <span class="alert-time" style="font-size: 12px; color: rgb(198, 52, 52) !important;">${date.getHours()} : ${date.getMinutes()}</span>
                             </div>
                             <span class="font-weight-bold" style="color: var(--sidebar-inside-color); font-size: 15px">
                                 您有 <span class="alert-total">1</span> 則新通知
                             </span>
                         </div>
                        </a>
                        `).prepend(`
                        <h6 class="dropdown-header header-h6 text-center" id="nav-alertcenter">
                            Alerts Center
                        </h6>
                        `);
                    } else {
                        let alertMessage = document.querySelectorAll('.alert-message');
                        /* ==2 代表訊息圖片圖示目前只有一個  ==3 有兩個 */ 
                        if (alertMessage[0].children.length === 2) {
                            if (alertMessage[0].children[0].getAttribute('data-item') !== 'image') {
                                $('.alert1 .alert-icon').addClass('alert-icon2').removeClass('alert-icon');
                                $('.alert1').prepend(`
                                <div class="icon-circle alert-icon alert-pos" style="background-color: var(--bg-1)"
                                data-item="image">
                                    <i class="fas fa-solid fa-image text-white"></i>
                                </div>  
                                `);
                            }
                        } else if (alertMessage[0].children.length === 3) {
                            if (alertMessage[0].children[0].getAttribute('data-item') !== 'image') {
                                $('.alert1 .alert-icon2').remove();
                                $('.alert1 .alert-icon').addClass('alert-icon2').removeClass('alert-pos alert-icon');
                                $('.alert1').prepend(`
                                <div class="icon-circle alert-icon alert-pos" style="background-color: var(--bg-1)"
                                data-item="image">
                                    <i class="fas fa-solid fa-image text-white"></i>
                                </div>  
                                `);
                            }
                        };
                        $('.alert1 .alert-date').text(dateString);
                        $('.alert1 .alert-time').text(`${date.getHours()} : ${minute_0}`);
                        $('.alert1 .alert-total').text(`${parseInt($('.alert1 .alert-total').text()) + 1}`);
                    } 

                    let alertQty = parseInt($('.alert-qty').text());
                    if (alertQty  === 0) {
                        $('.badge.badge-danger.badge-counter').text(1);
                    } else {
                        $('.badge.badge-danger.badge-counter').text(alertQty + 1)
                    }
                    
                    $('.alert-qty').text(`${alertQty + 1}`)

                }
            },
            error: function (data) {
                console.log("upload error", data);
                $('#staticBackdrop').modal('hide')
                setTimeout(() => {
                    Swal.fire({
                        icon: 'error',
                        color: '#fff',
                        background: 'cadetblue',
                        title: localStorage.getItem('language') === 'zh'
                                ? '發生未知錯誤'
                                : 'An unknown error occurred',
                    }).then(() => {
                        window.location.reload()
                    })
                }, 2000);
              },
        })
    }

    // 暫時解決不了用js新增的alert1按click跳頁新增localStorage
    $('.alert1').click(function () { 
        localStorage.setItem('alert', 'alert1')
    });

    groupBtn_rightBtn.onclick = () => {
        switchCard(0);
        $('.img-card').removeAttr('src');
        $('.group-btn').css('opacity', 0);
        $('.left-btn').attr('disabled', true);
        $('.right-btn').attr('disabled', true);
    }

    groupBtn2_leftBtn.onclick = () => {
        let element = document.createElement('a');
        element.setAttribute('href', $("#output_image").attr("src"));
        element.setAttribute('download', `${file_name}`)
        let imageDownload = document.querySelector('.image-download')
        imageDownload.appendChild(element)
        element.click()
        imageDownload.removeChild(element)
    }

    groupBtn2_rightBtn.onclick = () => {
        switchCard(0);
        $('.img-card').removeAttr('src');
        $('.group-btn').css('opacity', 0);
        $('.left-btn').attr('disabled', true);
        $('.right-btn').attr('disabled', true);
        $('.group-btn2').css('opacity', 0);
        $(".card2-img").addClass('d-none');
    }

});

loadImage = (file) => {
    let reader = new FileReader();
    reader.addEventListener('load', () => {
        $('.img-card').attr('src', reader.result);
    })

    if (file) {
        reader.readAsDataURL(file);
    }
};

switchCard = (pageNum) => {
    let containers = ['.first-container', '.second-container'];
    let visibleContainer = containers[pageNum];
    for (let i =0; i < containers.length; i++) {
        let oz = (containers[i] === visibleContainer) ? 1 : 0;
        $(containers[i]).animate({
            'opacity': oz,
            'z-index': oz,
        }, {
            duration: 400,
            queue: false,
        })
    }
};



