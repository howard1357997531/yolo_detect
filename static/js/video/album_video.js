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

  if (location.pathname.slice(7,18) !== localStorage.getItem('album_video_url')) {
    if (dateTarget === null) {
      alertify.warning(localStorage.getItem('language') === 'zh' ? '今日沒有新增影片' : 'No video added today');
    } 
    localStorage.setItem('album_video_url', 'album_video')
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
          url: "/video/album_video_search_ajax",
          data: {'dateInfo': dateInfo},
          success: function (response) {
            if (response.ok === 'success') {
              window.location = dateInfo;
            } else {
              Swal.fire({
                icon: 'warning',
                title: localStorage.getItem('language') === 'zh' 
                      ? `${$('.date_info').val()} 沒有儲存影片`
                      : `No image stored in ${$('.date_info').val()}`,
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
  
  // 手機模式的日期搜尋
  $('.datebtn2').click(function () { 
    $('.datebtn2').removeAttr('href');
    let datetime = document.querySelectorAll('.datetime')
    let dateInfo = $('.date_info2').val().replaceAll('-', '')
    if (!dateInfo) {
      Swal.fire({
          icon: 'warning',
          title: localStorage.getItem('language') === 'zh' ? `請選擇日期` : `Please select date`,
        })
      }
    let dateArray = [];
    datetime.forEach((el)=>{
      dateArray.push(el.id)
    })
    if (dateArray.includes(`d${dateInfo}`)) {
      $('.datebtn2').attr('href', `#d${dateInfo}`); //不能直接加在原本a裡面的herf,會有問題
      let element = document.createElement('a');
      let body = document.getElementsByTagName('body')[0];
      element.setAttribute('href', `#d${dateInfo}`)
      body.appendChild(element);
      setTimeout(() => {
        element.click(); // 其實.click()是針對button
        // click() 方法不會讓 <a> 元素和接收到真實滑鼠點擊一樣進行頁面跳轉。但不知為何在這邊可以
      body.removeChild(element);
      }, 800);
    } else {
      Swal.fire({
          icon: 'warning',
          title: localStorage.getItem('language') === 'zh'
                ? `${$('.date_info2').val()} 沒有儲存影片`
                : `No video stored in ${$('.date_info2').val()}`,
        })
      }
  });

  let all_download_btn = document.querySelectorAll('.album-video-download-all');
  all_download_btn.forEach(el => {
    el.addEventListener('click', e =>{
      e.preventDefault()
      $.ajax({
        type: "POST",
        url: "/video/album_video_download_all_ajax",
        data: {
          album_video_date: el.getAttribute('data-datetime'),
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        success: function (response) {
          if (response.ok === 'success') {
            let zip_download = document.querySelector(`.zip_download${el.getAttribute('data-date_id')}`);
            zip_download.click()
          }
        },
        error: function (data) {
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
      });
    })
  })

  let all_delete_btn = document.querySelectorAll('.album-video-delete-all');
  all_delete_btn.forEach(el => {
    el.addEventListener('click', (e)=>{
      e.preventDefault();
      Swal.fire({
      title: localStorage.getItem('language') === 'zh' ? '確定要刪除' : 'Sure to delete?',
      text: localStorage.getItem('language') === 'zh'
            ? `所有 ${el.getAttribute('data-datetime')} 的影片?`
            : `All ${el.getAttribute('data-datetime')} videos?`,
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
          url: "/video/album_video_delete_all_ajax",
          data: {
            album_video_date: el.getAttribute('data-datetime'),
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
                  title: localStorage.getItem('language') === 'zh' ? '成功!' : 'success',
                  text: localStorage.getItem('language') === 'zh'
                        ? `全部 ${el.getAttribute('data-datetime')} 的影片已刪除`
                        : `All ${el.getAttribute('data-datetime')} videos has been deleted.`,
                }).then(()=>{
                    localStorage.removeItem('album_video_url');      
                    $(`.photo-card${el.getAttribute('data-date-created')}`).slideUp(800);
                    setTimeout(() => {
                      $(`.photo-card${el.getAttribute('data-date-created')}`).remove();
                      let photo = document.querySelector('.photo');
                      if (photo.children.length === 3) {
                        $('#photo-empty').removeAttr('style');
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
  })
  
  let delete_btn = document.querySelectorAll('.album-video-modal-delete');
  delete_btn.forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      Swal.fire({
        title: localStorage.getItem('language') === 'zh' ? '確定要刪除?' : 'Sure to delete?',
        text: el.getAttribute('data-name'),
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
              url: "/video/album_video_delete_ajax",
              data: {
                album_video_id: el.getAttribute('data-id'),
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
                    title: localStorage.getItem('language') === 'zh' ? '成功!' : 'success',
                    text: localStorage.getItem('language') === 'zh' 
                          ? `${el.getAttribute('data-name')}  已刪除`
                          : `${el.getAttribute('data-name')}  has been deleted.`,
                  }).then(()=>{
                    $('.modal').modal('hide');
                    $(`.folder${el.getAttribute('data-id')}`).fadeOut(800);
                    setTimeout(() => {
                      $(`.folder${el.getAttribute('data-id')}`).remove();
                    }, 800);
                    
                    let photoDateCount = document.querySelector(`.f${el.getAttribute('data-date-created')}`)
                    if (photoDateCount.children.length === 1) {
                      $(`.photo-card${el.getAttribute('data-date-created')}`).slideUp(800);
                      setTimeout(() => {
                        $(`.photo-card${el.getAttribute('data-date-created')}`).remove();
                        let photo = document.querySelector('.photo');
                        if (photo.children.length === 3) {
                          $('#photo-empty').removeAttr('style');
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
            });
          }
        })
    })
  });

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

  let languageSelect = document.querySelectorAll('.language-select a')
  languageSelect.forEach((el) => {
      el.addEventListener('click', () => {
          if (el.classList.contains('language-en')) {
              $('.date_info, .date_info2').attr('placeholder', 'Please select date');
              $('.album-video-download-all').text('Download All');
              $('.album-video-delete-all').text('Delete All');
              // modal
              $('.t-hour').text('h');
              $('.t-minute').text('m');
              $('.t-second').text('s');
              $('.album-video-modal-download').text('Download');
              $('.album-video-modal-delete').text('Delete');
          } else {
              $('.date_info, .date_info2').attr('placeholder', '請選擇日期');
              $('.album-video-download-all').text('下載全部');
              $('.album-video-delete-all').text('刪除全部');
              // modal
              $('.t-hour').text('時');
              $('.t-minute').text('分');
              $('.t-second').text('秒');
              $('.album-video-modal-download').text('下載');
              $('.album-video-modal-delete').text('刪除');
          }
      })
  })

  if (localStorage.getItem('language') === 'zh') {
    $('.date_info, .date_info2').attr('placeholder', '請選擇日期');
    $('.album-video-download-all').text('下載全部');
    $('.album-video-delete-all').text('刪除全部');
    // modal
    $('.t-hour').text('時');
    $('.t-minute').text('分');
    $('.t-second').text('秒');
    $('.album-video-modal-download').text('下載');
    $('.album-video-modal-delete').text('刪除');
}
});


