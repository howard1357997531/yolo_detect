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
  // console.log(dateTarget.getBoundingClientRect().y)
  // console.log(dateTarget)
  // 會自動拉到今日日期
  // if (dateTarget !== null) {    
  //   if (localStorage.getItem('photo_position')) {
  //     window.scrollTo({
  //       top: parseFloat(localStorage.getItem('photo_position')),
  //     });
  //   } else {
  //     window.scrollTo({
  //       top: dateTarget.getBoundingClientRect().y,
  //     });
  //     localStorage.setItem('photo_position', String(dateTarget.getBoundingClientRect().y))
  //   }

  //   /*
  //   // 如果只是寫這樣，reload會跑到最上面
  //   // 隨便向上滑動到某個位置，reload後不會回到今日日期位置(最低點)，會到比較上面的位置
  //   // 因為 getBoundingClientRect().y  是看'當前網頁位置'到div的距離
  //   // 所以上面才會把第一次進到頁面的y軸距離存起來，之後reload到會到那個距離
  //   window.scrollTo({
  //     top: dateTarget.getBoundingClientRect().y,
  //   });
  //   */
  // }
  // console.log(location.pathname) //  /album/
  // 只有第一次進入網頁會顯示
  if (location.pathname.slice(7,12) !== localStorage.getItem('photo_url')) {
    if (dateTarget === null) {
      alertify.warning(localStorage.getItem('language') === 'zh' ? '今日沒有新增影片' : 'No video added today');
    } 
    localStorage.setItem('photo_url', 'photo')
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
          element.click(); // 其實.click()是針對button
          // click() 方法不會讓 <a> 元素和接收到真實滑鼠點擊一樣進行頁面跳轉。但不知為何在這邊可以
        body.removeChild(element);
        }, 800);
      } else {
        $.ajax({
          type: "GET",
          url: "/image/photo_search_ajax",
          data: {'dateInfo': dateInfo},
          success: function (response) {
            if (response.ok === 'success') {
              window.location = dateInfo;
            } else {
              Swal.fire({
                icon: 'warning',
                title: localStorage.getItem('language') === 'zh' 
                      ? `${$('.date_info').val()} 沒有儲存圖片`
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
          title: localStorage.getItem('language') === 'zh' 
                ? `請選擇日期`
                : `Please select date`,
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
              ? `${$('.date_info2').val()} 沒有儲存圖片`
              : `No image stored in ${$('.date_info2').val()}`,
      })
    }
  });

  let all_download_btn = document.querySelectorAll('.photo-download-all');
  all_download_btn.forEach(el=>{
    el.addEventListener('click',(e)=>{
      e.preventDefault()
      $.ajax({
        type: "POST",
        url: "/image/photo_download_all_ajax",
        data: {
          photo_date: el.getAttribute('data-datetime'),
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

  let all_delete_btn = document.querySelectorAll('.photo-delete-all');
  all_delete_btn.forEach(el=>{
    el.addEventListener('click', (e)=>{
      e.preventDefault();
      console.log(el.getAttribute('data-datetime'))
      Swal.fire({
      title: localStorage.getItem('language') === 'zh' ? '確定要刪除?' : 'Sure to delete?',
      text: localStorage.getItem('language') === 'zh'
          ? `所有 ${el.getAttribute('data-datetime')} 的照片?`
          : `All ${el.getAttribute('data-datetime')} images?`,
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
          url: "/image/photo_delete_all_ajax",
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
                        ? `全部 ${el.getAttribute('data-datetime')} 的照片已刪除`
                        : `All ${el.getAttribute('data-datetime')} images has been deleted.`,
                }).then(()=>{
                  localStorage.removeItem('photo_url');
                  $(`.photo-card${el.getAttribute('data-date-created')}`).slideUp(800);
                  setTimeout(() => {
                    $(`.photo-card${el.getAttribute('data-date-created')}`).remove();
                    let photo = document.querySelector('.photo');
                    if (photo.children.length === 3) {
                      $('#photo-empty').removeAttr('style');
                    }
                  }, 800);
                })
              };
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

  let photoDeleteBtn = document.querySelectorAll('.photo-modal-delete');
  photoDeleteBtn.forEach(el => {
    el.addEventListener('click', () => {
      console.log(el.getAttribute('data-id'))
      Swal.fire({
        title: localStorage.getItem('language') === 'zh' ? '確定要刪除?' : 'Sure to delete?',
        text: `${el.getAttribute('data-name')}`,
        color: '#fff',
        background: 'cadetblue',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: 'rgb(99, 57, 190)',
        confirmButtonText: localStorage.getItem('language') === 'zh' ? '刪除' : 'Delete',
        cancelButtonText: localStorage.getItem('language') === 'zh' ? '返回' : 'Back',
        }).then((result) => {
          if (result.isConfirmed) {
            $.ajax({
              type: "POST",
              url: "/image/photo_delete_ajax",
              data: {
                  id: el.getAttribute('data-id'),
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

                      let photoDateCount = document.querySelector(`.f${el.getAttribute('data-date-created')}`);
                      if (photoDateCount.children.length === 1) {
                        $(`.photo-card${el.getAttribute('data-date-created')}`).slideUp(800);
                        setTimeout(() => {
                          $(`.photo-card${el.getAttribute('data-date-created')}`).remove();
                          let photo = document.querySelector('.photo');
                          if (photo.children.length === 3) {
                            $('#photo-empty').removeAttr('style');
                          }
                        }, 800);
                      };                  
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
          });
    })
  })

  let photoDownloadBtn = document.querySelectorAll('.photo-modal-download');
  photoDownloadBtn.forEach(el => {
    el.addEventListener('click', () => {
      console.log(el.getAttribute('data-id'))
    })
  })

  let photo = document.querySelectorAll('.folderasd');
  photo.forEach(el => {
    el.addEventListener('click', ()=> {
      Swal.fire({
        text: el.getAttribute('data-name'),
        imageUrl: el.getAttribute('data-url'),
        width: width,
        color: '#fff',
        background: 'cadetblue',
        imageWidth: imageWidth,
        imageHeight: imageHeight,
        imageAlt: 'Custom image',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonColor: '#d33',
        denyButtonColor: '#000',
        cancelButtonColor: 'rgb(99, 57, 190)',
        confirmButtonText: localStorage.getItem('language') === 'zh' ? '刪除' : 'Delete',
        denyButtonText: localStorage.getItem('language') ? '下載' : 'Download',
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
            }).then((result) => {
              if (result.isConfirmed) {
                $.ajax({
                  type: "POST",
                  url: "/image/photo_detail_delete_ajax",
                  data: {
                      id: el.getAttribute('data-id'),
                  },
                  beforeSend: function(xhr, settings) {
                      xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                  },
                  success: function (response) {
                      if (response.ok === 'success') {
                          Swal.fire(
                              localStorage.getItem('language') === 'zh' ? '成功!' : 'success',
                              localStorage.getItem('language') === 'zh' 
                                  ? `${el.getAttribute('data-name')}  已刪除`
                                  : `${el.getAttribute('data-name')}  has been deleted.`,
                              'success'
                              ).then(()=>{
                                  window.location.href = location.origin + '/image/photo'
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
                      }).then(() => {
                          window.location.reload()
                      })
                      }, 2000);
                  },
                  });
                }
              });
          
        } else if (result.isDenied) {
          let a = document.querySelector(`.photo-download-id${el.getAttribute('data-id')}`)
          a.click()
          Swal.fire({
            icon: 'success',
            title: localStorage.getItem('language') ? '下載成功' : 'Download successfully',
            color: '#fff',
            background: 'cadetblue'
          })
        }
      })
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

  let languageSelect = document.querySelectorAll('.language-select a')
  languageSelect.forEach((el) => {
      el.addEventListener('click', () => {
          if (el.classList.contains('language-en')) {
              $('.date_info, .date_info2').attr('placeholder', 'Please select date');
              $('.photo-download-all').text('Download All');
              $('.photo-delete-all').text('Delete All');
              // modal
              $('.t-hour').text('h');
              $('.t-minute').text('m');
              $('.t-second').text('s');
              $('.photo-modal-download').text('Download');
              $('.photo-modal-delete').text('Delete');
          } else {
              $('.date_info, .date_info2').attr('placeholder', '請選擇日期');
              $('.photo-download-all').text('下載全部');
              $('.photo-delete-all').text('刪除全部');
              // modal
              $('.t-hour').text('時');
              $('.t-minute').text('分');
              $('.t-second').text('秒');
              $('.photo-modal-download').text('下載');
              $('.photo-modal-delete').text('刪除');
          }
      })
  })

  if (localStorage.getItem('language') === 'zh') {
    $('.date_info, .date_info2').attr('placeholder', '請選擇日期');
    $('.photo-download-all').text('下載全部');
    $('.photo-delete-all').text('刪除全部');
    // modal
    $('.t-hour').text('時');
    $('.t-minute').text('分');
    $('.t-second').text('秒');
    $('.photo-modal-download').text('下載');
    $('.photo-modal-delete').text('刪除');
}
});


