$(document).ready(function () {
  let body = document.querySelectorAll('body')[0]
  let dropzone = document.querySelector('.dropzone')

  body.ondrop = body.ondragover = body.ondragend = () => {
    return false
  }

  // 如果取得<div class="dz-preview dz-processing dz-success dz-complete dz-image-preview"> 裡面的img base64圖片會很小張
  // 因為那些是被裁切過得(120*120),要去取得下面 <input class="dz-hidden-input"> 裡面的base64,為完整圖片大小

  var formData = {};
  $('.dz-hidden-input').change(function (e) {
    console.log(e.target.files.length)
    // console.log(e.target.files[0].name)
    if (e.target.files.length >100) {
      if (localStorage.getItem('language') === 'zh') {
        Swal.fire({
            icon: 'warning',
            title: localStorage.getItem('language') === 'zh' ? '最多上傳100張照片' : 'Upload up to 100 photos',
          })
        }
    }
    
    for (let i = 0; i < e.target.files.length; i++) {
      let reader = new FileReader() // 每次需要建立新的reader,不然會error
      reader.onload = () => {
        formData[`base64_${i+1}`] = reader.result;
        formData[`image_name_${i+1}`] = e.target.files[i].name;
      }
      reader.readAsDataURL(e.target.files[i])
    }
    $('.web-camera-groupbtn').css('display', 'flex');
  });

  dropzone.ondrop = (e) => {
    // console.log(e.dataTransfer.files.length)
    for (let i = 0; i < e.dataTransfer.files.length; i++) {
      console.log(e.dataTransfer.files[i])
      let reader = new FileReader() 
      let name = e.dataTransfer.files[i].name  // 使用ondrop時，e.dataTransfer.files[i].name
      reader.onload = () => {                  // 不知為何不能寫在onload裡面
        formData[`base64_${i+1}`] = reader.result;
        formData[`image_name_${i+1}`] = name;
      }
      reader.readAsDataURL(e.dataTransfer.files[i])
    }
    $('.web-camera-groupbtn').css('display', 'flex');
  }

  $('#image-multiple-openbtn').click(() => {
    // Object.keys(formData) 把物件key回傳承成 array
    let photoQty = Object.keys(formData).length / 2;
    let photoSaveToAlbumLimit = $('#amount').text();

    if (photoQty <= parseInt(photoSaveToAlbumLimit)) {
      Swal.fire({
        title: localStorage.getItem('language') === 'zh' 
              ? `偵測照片低於 ${photoSaveToAlbumLimit} 張`
              : `Detect image lower than ${photoSaveToAlbumLimit}`,
        text: localStorage.getItem('language') === 'zh' 
              ? '是否要同步新增照片到 "相簿" ?'
              : 'Do you also want to save photos to the album ?',
        icon: 'info',
        color: '#fff',
        background: 'cadetblue',
        showCancelButton: true,
        confirmButtonColor: 'rgb(99, 57, 190)',
        cancelButtonColor: '#d33',
        confirmButtonText: localStorage.getItem('language') === 'zh' ? '是' : 'Yes',
        cancelButtonText: localStorage.getItem('language') === 'zh' ? '否' : 'No',
      }).then((result) => {
        $('#staticBackdrop').modal('show');
        formData['save_to_album'] = result.isConfirmed ? 'yes' : 'no'
        $.ajax({
          url: "/image_multiple_folder_ajax",
          type: "POST",
          data: formData,
          beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
          },
          success: function (response) {
            $('#staticBackdrop').modal('hide');
            if (response.ok === 'success') {
              Swal.fire({
                icon: 'success',
                color: '#fff',
                background: 'cadetblue',
                title: localStorage.getItem('language') === 'zh' ? '圖片全部處理完成' : 'All Image has been done',
              }).then(() => {
                window.location.reload()
              })
            }
          },
          error: function (data) {
            setTimeout(() => {
              $('#staticBackdrop').modal('hide');
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
      })
    } else {
      $('#staticBackdrop').modal('show');
      formData['save_to_album'] = 'no';
      $.ajax({
        url: "/image_multiple_folder_ajax",
        type: "POST",
        data: formData,
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        success: function (response) {
          $('#staticBackdrop').modal('hide');
          if (response.ok === 'success') {
            Swal.fire({
              icon: 'success',
              color: '#fff',
              background: 'cadetblue',
              title: localStorage.getItem('language') === 'zh' ? '圖片全部處理完成' : 'All Image has been done',
            }).then(() => {
              window.location.reload()
            })
          }
        },
        error: function (data) {
          setTimeout(() => {
            $('#staticBackdrop').modal('hide');
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
  })

  $('.tool-icon').click(function () { 
    if ($('.tool').css('display') === 'none') {
      $('.tool').slideDown();
    } else {
      $('.tool').slideUp();
    }
  });

  $('.yolo-image-multiple .right-btn').click(function () { 
    window.location.reload()
  });

  $('.dz-button').attr('id', 'image-multiple-dz-button');
});



Dropzone.options.myDropzone = {
  uploadMultiple: true,
  parallelUploads: 100,
  maxFiles: 100,
  acceptedFiles: 'image/*',
  //createImageThumbnails: false,
  // thumbnailWidth: null,
  // thumbnailHeight: null,
  //addRemoveLinks:true,
};  
