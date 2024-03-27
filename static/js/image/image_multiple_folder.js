$(document).ready(function () {
  if (localStorage.getItem('language')) {
    $('.date_info').attr('placeholder', '請選擇日期');
    $('.date_info2').attr('placeholder', '請選擇日期');
  };

  // 取得今日日期 ex:20230506
  const date = new Date()
  let month_0 = date.getMonth() < 9 ? '0' + String(parseInt(date.getMonth())+1) : String(parseInt(date.getMonth())+1)
  let date_0 = date.getDate() < 10 ? '0' + String(parseInt(date.getDate())) : String(parseInt(date.getDate()))
  let dateString = date.getFullYear() + month_0 + date_0
  let dateTarget = document.querySelector(`#d${dateString}`)

  if (location.pathname.slice(7,28) !== localStorage.getItem('image_multiple_folder_url')) {
    if (dateTarget === null) {
      alertify.warning(localStorage.getItem('language') === 'zh' ? '今日沒有新增資料夾' : 'No folder added today');
    } 
    localStorage.setItem('image_multiple_folder_url', 'image_multiple_folder')
  }
  
  $('.datebtn').click(function () { 
    $('.datebtn').removeAttr('href');
    let dateInfo = $('.date_info').val().replaceAll('-', '');
    if (!dateInfo) {
      Swal.fire({
          icon: 'warning',
          title: localStorage.getItem('language') === 'zh' ? `請選擇日期` : `Please select date`,
          color: '#fff',
          background: 'cadetblue',
        })
    } else {
      let datetime = document.querySelectorAll('.datetime');
      let dateArray = [];
      datetime.forEach((el)=>{
        dateArray.push(el.id)
      })
      if (dateArray.includes(`d${dateInfo}`)) {
        $('.container-fluid').css('min-height', '160vh');
        $('.datebtn').attr('href', `#d${dateInfo}`); //不能直接加在原本a裡面的herf,會有問題
        let element = document.createElement('a');
        let body = document.getElementsByTagName('body')[0];
        element.setAttribute('href', `#d${dateInfo}`)
        body.appendChild(element);
        setTimeout(() => {
          element.click();
        body.removeChild(element);
        }, 800);
      } else {
        $.ajax({
          type: "GET",
          url: "/image/image_multiple_folder_search_ajax",
          data: {'dateInfo': dateInfo},
          success: function (response) {
            if (response.ok === 'success') {
              window.location = dateInfo;
            } else {
              Swal.fire({
                icon: 'warning',
                title: localStorage.getItem('language') === 'zh' 
                      ? `${$('.date_info').val()} 沒有儲存資料夾`
                      : `No folder stored in ${$('.date_info').val()}`,
                color: '#fff',
                background: 'cadetblue',
              })
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
        
      }
    }
  });

  let photoBtn = document.querySelectorAll('.photo_btn');
  photoBtn.forEach(el => {
    el.addEventListener('click', () => {
      let tr = document.querySelectorAll(`.table${el.getAttribute('data-photo-code')} tr`)
      if (window.innerWidth >= 768) {
        var width = '800px';
        var imageWidth = 600;
        var imageHeight = 400;
      } else if (window.innerWidth > 500) {
        var width = '500px';
        var imageWidth = 400;
        var imageHeight = 266;
      } else {
        var width = '370px';
        var imageWidth = 300;
        var imageHeight = 200;
      }
      Swal.fire({
        text: el.innerText,
        imageUrl: el.getAttribute('data-url'),
        width: width,
        color: '#fff',
        background: 'cadetblue',
        imageWidth: imageWidth,
        imageHeight: imageHeight,
        imageAlt: 'Custom image',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: 'rgb(99, 57, 190)',
        confirmButtonText: localStorage.getItem('language') === 'zh' ? '刪除' : 'Delete',
        cancelButtonText: localStorage.getItem('language') === 'zh' ? '返回' : 'Back',
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: localStorage.getItem('language') === 'zh' ? '確定要刪除?' : 'Sure to delete?',
            text: el.innerText,
            color: '#fff',
            background: 'cadetblue',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: 'rgb(99, 57, 190)',
            confirmButtonText: localStorage.getItem('language') === 'zh' ? '刪除' : 'Delete',
            cancelButtonText: localStorage.getItem('language') === 'zh' ? '返回' : 'Back',
            })
            .then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                type: "POST",
                url: "/image/image_multiple_folder_delete_ajax",
                data: {
                  photo_id: el.getAttribute('data-photo-id'),
                },
                beforeSend: function(xhr, settings) {
                  xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                },
                success: function (response) {
                  if (response.ok === 'success') {
                    Swal.fire({
                      icon: 'success',
                      color: '#fff',
                      background: 'cadetblue',
                      title: localStorage.getItem('language') === 'zh' ? '成功!' : 'Success!',
                      text: localStorage.getItem('language') === 'zh' 
                            ? `${el.innerText}  已刪除`
                            : `${el.innerText}  has been deleted.`,
                    }).then(()=>{
                        $(`.photo-code${el.getAttribute('data-photo-code')}`).text(`${tr.length - 1}`);
                        $(`.img${el.getAttribute('data-photo-id')}`).fadeOut(800);
                        setInterval(() => {
                          $(`.img${el.getAttribute('data-photo-id')}`).remove()
                        }, 800);
                        if (tr.length === 1){
                          $(`#Modal${el.getAttribute('data-photo-code')}`).modal('hide');
                          $(`.folder${el.getAttribute('data-photo-code')}`).fadeOut(800);
                          setInterval(() => {
                            $(`.folder${el.getAttribute('data-photo-code')}`).remove()
                          }, 800);
                        }
                        
                        let f_date = document.querySelector(`.f${el.getAttribute('data-date-created')}`)
                        let table = document.querySelector(`.table${el.getAttribute('data-photo-code')}`)
                        if (f_date.children.length ===1 && table.children[0].children.length === 1) {
                          $(`.photo-card${el.getAttribute('data-date-created')}`).slideUp(800);
                          setTimeout(() => {
                            $(`.photo-card${el.getAttribute('data-date-created')}`).remove();
                            let photo = document.querySelector('.photo');
                            if (photo.children.length === 3) {
                              $('#image-multiple-folder-empty').removeAttr('style');
                            }
                          }, 800);
                        }
                      })
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
                      })
                    }, 2000);
                },
              });
            } 
          })
          
        }
      })
    })
  });

  let photoDeleteAllForDayBtn = document.querySelectorAll('.image-multiple-folder-modal-delete-all');
  photoDeleteAllForDayBtn.forEach(el => {
    el.addEventListener('click', () => {
      let tr = document.querySelectorAll(`.table${el.getAttribute('data-photo-code')} tr`);
      let photoIdArray = [];
      tr.forEach((inner_el)=>{
        photoIdArray.push(inner_el.children[0].children[0].getAttribute('data-photo-id'));
      })
      console.log(photoIdArray)
      Swal.fire({
        title: localStorage.getItem('language') === 'zh'
            ? `確定要刪除?`
            : `Sure to delete?`,
        text: localStorage.getItem('language') === 'zh' 
            ? `此資料夾裡面所有的照片?`
            : `All the images in this folder`,
        icon: 'warning',
        color: '#fff',
        background: 'cadetblue',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: 'rgb(99, 57, 190)',
        confirmButtonText: localStorage.getItem('language') === 'zh' ? '刪除' : 'Delete',
        cancelButtonText: localStorage.getItem('language') === 'zh' ? '返回' : 'Back',
      }).then((result) => {
        if (result.isConfirmed) {
          $.ajax({
            type: "POST",
            url: "/image/image_multiple_folder_delete_all_ajax",
            data: {
              'photo_id_array': JSON.stringify(photoIdArray),
            },
            beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            },
            success: function (response) {
              if (response.ok === 'success') {
                Swal.fire({
                  icon: 'success',
                  color: '#fff',
                  background: 'cadetblue',
                  title: localStorage.getItem('language') === 'zh' ? '成功!' : 'Success!',
                  text: localStorage.getItem('language') === 'zh'
                        ? `全部的照片已刪除`
                        : `All images has been deleted.`,
                }).then(()=>{
                  $(`#Modal${el.getAttribute('data-photo-code')}`).modal('hide');
                  $(`.folder${el.getAttribute('data-photo-code')}`).fadeOut(800);
                  setTimeout(() => {
                    $(`.folder${el.getAttribute('data-photo-code')}`).remove()
                  }, 800);
                  let f_date = document.querySelector(`.f${el.getAttribute('data-date-created')}`)
                  if (f_date.children.length === 1) {
                    $(`.photo-card${el.getAttribute('data-date-created')}`).slideUp(800);
                    setTimeout(() => {
                      $(`.photo-card${el.getAttribute('data-date-created')}`).remove();
                      let photo = document.querySelector('.photo');
                        if (photo.children.length === 3) {
                          $('#image-multiple-folder-empty').removeAttr('style');
                        }
                    }, 800);
                  };
                  
                }) 
              }
            },
            error: function (data) {
                $('#staticBackdrop').modal('hide')
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
        }
      })
    })
  });
  
  let photoDeleteAllBtn = document.querySelectorAll('.photo-delete-all');
  photoDeleteAllBtn.forEach(el => {
    el.addEventListener('click', () => {
      Swal.fire({
        title: localStorage.getItem('language') === 'zh' ? '確定要刪除?' : 'Sure to delete?',
        text: localStorage.getItem('language') === 'zh'
            ? `所有 ${el.getAttribute('data-datetime')} 的資料夾?`
            : `All ${el.getAttribute('data-datetime')} folder?`,
        color: '#fff',
        background: 'cadetblue',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: 'rgb(99, 57, 190)',
        confirmButtonText: localStorage.getItem('language') === 'zh' ? '刪除' : 'Delete',
        cancelButtonText: localStorage.getItem('language') === 'zh' ? '返回' : 'Back',
        })
        .then((result) => {
        if (result.isConfirmed) {
          $.ajax({
            type: "POST",
            url: "/image/image_multiple_folder_delete_all_for_day_ajax",
            data: {
              photo_date: el.getAttribute('data-datetime'),
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            },
            success: function (response) {
                if (response.ok === 'success') {
                  Swal.fire({
                    icon: 'success',
                    color: '#fff',
                    background: 'cadetblue',
                    title: localStorage.getItem('language') === 'zh' ? '成功!' : 'Success!',
                    text: localStorage.getItem('language') === 'zh'
                          ? `全部的照片已刪除`
                          : `All images has been deleted.`,
                  }).then(()=>{
                    $(`.photo-card${el.getAttribute('data-date-created')}`).slideUp(800);
                    setTimeout(() => {
                      $(`.photo-card${el.getAttribute('data-date-created')}`).remove();
                      let photo = document.querySelector('.photo');
                      if (photo.children.length === 3) {
                        $('#image-multiple-folder-empty').removeAttr('style');
                      }
                    }, 800);
                  })
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
          }
        })
    })
  });

  let photoDownloadAllBtn = document.querySelectorAll('.image-multiple-folder-modal-download-all');
  photoDownloadAllBtn.forEach(el => {
    el.addEventListener('click', () => {
      console.log(el.getAttribute('data-photo-code'))
      $.ajax({
        type: "POST",
        url: "/image/image_multiple_folder_download_all_ajax",
        data: {
          photo_code: el.getAttribute('data-photo-code'),
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        success: function (response) {
            if (response.ok === 'success') {
              zip_download = document.querySelector(`.zip_download${el.getAttribute('data-photo-code')}`);
              zip_download.click()
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
    })
  })

  $('.photo-search').on('input', function () {
    let text = $(this).val().trim();
    let table = document.querySelector(`.table${$(this).data('code')}`);
    let tr = table.children[0].children;
    let count = 0;

    tr.forEach(el => {
      let filename = el.children[0].children[0].innerText;
      // . 表示任意值，用此方法解決
      let escapeText = text.replace(/\./g, '\\.');
      let re = new RegExp(`${escapeText}`);
      
      if (filename.match(re)) {
        el.removeAttribute('style');
        count += 1;
      } else {
        el.style.display = 'none';
      }
    })
    $(`.photo-code${$(this).data('code')}`).text(count);
  });

  let folder = document.querySelectorAll('.folder');
  folder.forEach(el => {
    el.addEventListener('click', () => {
      $('.photo-search').val('');
      let table = document.querySelector(`.table${el.getAttribute('data-code')}`);
      let tr = table.children[0].children;
      tr.forEach(inner_el => {
        inner_el.removeAttribute('style');
      });

      $(`.photo-code${el.getAttribute('data-code')}`).text(table.children[0].children.length);
    })
  })
  
  $('#sidebarToggleTop').click(function () {
    if ($('.navbar-nav.sidebar').hasClass('toggled')) { //關閉
        if (window.innerWidth > 647 && window.innerWidth <= 767) {
            $('.folder').addClass('wh19');
            $('.folder .fas.fa-folder').css('font-size', '50px')
        } else if (window.innerWidth > 560 && window.innerWidth <= 647) {
            $('.folder').addClass('wh18-5');
            $('.folder .fas.fa-folder').css('font-size', '40px')
        } else if (window.innerWidth > 489 && window.innerWidth <= 560) {
            $('.folder').addClass('wh38');
            $('.folder .fas.fa-folder').css('font-size', '75px')
        } else if (window.innerWidth > 440 && window.innerWidth <= 489) {
            $('.folder').addClass('wh39');
            $('.folder .fas.fa-folder').css('font-size', '75px')
        } else if (window.innerWidth > 400 && window.innerWidth <= 440) {
            $('.folder').addClass('wh38_2');
            $('.folder .fas.fa-folder').css('font-size', '60px')
        } else if (window.innerWidth <= 400) {
            $('.folder').addClass('wh38_3');
            $('.folder .fas.fa-folder').css('font-size', '60px')
        }
    } else {
        if (window.innerWidth > 647 && window.innerWidth <= 767) {
            $('.folder').removeClass('wh19');
            $('.folder .fas.fa-folder').removeAttr('style');
        } else if (window.innerWidth > 560 && window.innerWidth <= 647) {
            $('.folder').removeClass('wh18-5');
            $('.folder .fas.fa-folder').removeAttr('style');
        } else if (window.innerWidth > 489 && window.innerWidth <= 560) {
            $('.folder').removeClass('wh38');
            $('.folder .fas.fa-folder').removeAttr('style');
        } else if (window.innerWidth > 440 && window.innerWidth <= 489) {
            $('.folder').removeClass('wh39');
            $('.folder .fas.fa-folder').removeAttr('style');
        } else if (window.innerWidth > 400 && window.innerWidth <= 440) {
            $('.folder').removeClass('wh38_2');
            $('.folder .fas.fa-folder').removeAttr('style');
        } else if (window.innerWidth <= 400) {
            $('.folder').removeClass('wh38_3');
            $('.folder .fas.fa-folder').removeAttr('style');
        }
    }
  });

  $('.sidebar-downbtn').click(function () { 
    if ($('.navbar-nav.sidebar').hasClass('toggled')) { //關閉
        if (window.innerWidth > 1840 ) {
            $('.folder').addClass('wh9');
        } else if (window.innerWidth > 1669 && window.innerWidth <= 1840) {
            $('.folder').addClass('wh8-85');
        } else if (window.innerWidth > 1534 && window.innerWidth <= 1669) {
            $('.folder').addClass('wh11-65');
        } else if (window.innerWidth > 1442 && window.innerWidth <= 1534) {
            $('.folder').addClass('wh11-4');
        } else if (window.innerWidth > 1283 && window.innerWidth <= 1442) {
            $('.folder').addClass('wh13');
        } else if (window.innerWidth > 1110 && window.innerWidth <= 1283) {
            $('.folder').addClass('wh15-3');
        } else if (window.innerWidth > 1021 && window.innerWidth <= 1110) {
            $('.folder').addClass('wh15');
        } else if (window.innerWidth > 946 && window.innerWidth <= 1021) {
            $('.folder').addClass('wh14-8');
        } else if (window.innerWidth > 847 && window.innerWidth <= 946) {
            $('.folder').addClass('wh18-2');
        } else if (window.innerWidth > 767 && window.innerWidth <= 847) {
            $('.folder').addClass('wh17-8');
        }
        $('.folder .fas.fa-folder').css('font-size', '70px')
    } else {
        if (window.innerWidth > 1840 ) {
            $('.folder').removeClass('wh9');
        } else if (window.innerWidth > 1669 && window.innerWidth <= 1840) {
            $('.folder').removeClass('wh8-85');
        } else if (window.innerWidth > 1534 && window.innerWidth <= 1669) {
            $('.folder').removeClass('wh11-65');
        } else if (window.innerWidth > 1442 && window.innerWidth <= 1534) {
            $('.folder').removeClass('wh11-4');
        } else if (window.innerWidth > 1283 && window.innerWidth <= 1442) {
            $('.folder').removeClass('wh13');
        } else if (window.innerWidth > 1110 && window.innerWidth <= 1283) {
            $('.folder').removeClass('wh15-3');
        } else if (window.innerWidth > 1021 && window.innerWidth <= 1110) {
            $('.folder').removeClass('wh15');
        } else if (window.innerWidth > 946 && window.innerWidth <= 1021) {
            $('.folder').removeClass('wh14-8');
        } else if (window.innerWidth > 847 && window.innerWidth <= 946) {
            $('.folder').removeClass('wh18-2');
        } else if (window.innerWidth > 767 && window.innerWidth <= 847) {
            $('.folder').removeClass('wh17-8');
        }
        $('.folder .fas.fa-folder').removeAttr('style')
      }
    }
  );

  let languageSelect = document.querySelectorAll('.language-select a');
  languageSelect.forEach((el) => {
    el.addEventListener('click', () => {
        if (el.classList.contains('language-en')) {
            $('.date_info, .date_info2').attr('placeholder', 'Please select date');
            $('.photo-delete-all').text('Delete All');
            $('.photo-search').attr('placeholder', 'Search');
            $('.image-multiple-folder-modal-span1').text('');
            $('.image-multiple-folder-modal-span2').text('photos in total');
            $('.image-multiple-folder-modal-download-all').text('Download All');
            $('.image-multiple-folder-modal-delete-all').text('Delete All');
        } else {
            $('.date_info, .date_info2').attr('placeholder', '請選擇日期');
            $('.photo-delete-all').text('刪除全部');
            $('.photo-search').attr('placeholder', '搜尋');
            $('.image-multiple-folder-modal-span1').text('共');
            $('.image-multiple-folder-modal-span2').text('張照片');
            $('.image-multiple-folder-modal-download-all').text('下載全部');
            $('.image-multiple-folder-modal-delete-all').text('刪除全部');
        }
    })
  });

  if (localStorage.getItem('language') === 'zh') {
    $('.date_info, .date_info2').attr('placeholder', '請選擇日期');
    $('.photo-delete-all').text('刪除全部');
    $('.photo-search').attr('placeholder', '搜尋');
    $('.image-multiple-folder-modal-span1').text('共')
    $('.image-multiple-folder-modal-span2').text('張照片');
    $('.image-multiple-folder-modal-download-all').text('下載全部');
    $('.image-multiple-folder-modal-delete-all').text('刪除全部');
  }
});
