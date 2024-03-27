$(document).ready(function () {
  let body = document.getElementsByTagName('body')[0];
  let uploadFile = document.querySelector('#file');
  let loading_icon = document.querySelector('.yolo-video .loading-icon');
  let loading_text = document.querySelector('.yolo-video .loading-text');
  let groupBtn_lefttBtn = document.querySelector('.group-btn .left-btn');
  let groupBtn_rightBtn = document.querySelector('.group-btn .right-btn');

  uploadFile.addEventListener('change', () => {
    console.log(uploadFile.files[0])
      if (uploadFile.files[0]) {
          $('.group-btn').css('opacity', 1);
          $('.left-btn').removeAttr('disabled');
          $('.right-btn').removeAttr('disabled');
          $('.text').text(`${uploadFile.files[0].name}`);
      }
  })

  body.ondragover = body.ondragend = body.ondrop = () => {
      return false;
  }
  
  groupBtn_lefttBtn.onclick = (e) => {
      e.preventDefault()
      input = $("#file")[0];
      console.log(input.files[0])
      console.log(input.files[0].name)
      let formData = new FormData();
      formData.append('name', input.files[0].name);
      formData.append('file', input.files[0]);
      $('.yolo-video .upload_button').attr('style', 'display:none')
      $('.yolo-video .text').attr('style', 'display:none')
      loading_icon.style.display = 'block'
      loading_text.style.display = 'block'
      if (input.files && input.files[0]) {
        $.ajax({
          url: "/get_video", 
          type: "POST",
          data: formData,
          processData: false,
          contentType: false,
          beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
          },
          success: function (response) {
            if (response.ok === 'success') {
              $('.card1').append(`<img src="/video_video_feed" 
                                          class="video_output" 
                                          alt=""></img>`);
              function handleStreamResponse(response) {
                const reader = response.body.getReader();
                
                function read() {
                  return reader.read().then(({ done, value }) => {
                    if (done) {
                      // 串流結束
                      // 目前不知為何會 Fusing layers 兩次，所以count是從3開始算，因此會提早到done這邊
                      // 所以用此方法來延緩時間
                      setTimeout(() => {
                        $.ajax({
                          type: "POST",
                          url: "/video_merge_ajax",
                          data: {
                            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                          },
                          success: function (response) {
                            if (response.ok === 'success'){
                              console.log('here')
                            }
                          }
                        });
                      }, 2000);

                      Swal.fire({
                        icon: 'success',
                        title: localStorage.getItem('language') === 'zh'
                                ? '已儲存'
                                : 'Save ! !',
                        color: '#fff',
                        background: 'cadetblue',
                      }).then(() => {
                          window.location.reload()
                      })
                      return;
                    }
                    
                    const text = new TextDecoder("utf-8").decode(value);
                    
                    // 在這裡處理每個串流數據
                    //console.log(text);
                    
                    // 檢查是否為串流結束標記
                    if (text.trim() === 'Finished') {
                      console.log("Stream finished.");
                      return;
                    }

                    // 繼續讀取下一個串流數據
                    return read();
                  });
                }
                
                // 開始讀取串流回應
                read();
              }
              
              // 發送 Fetch 請求
              fetch('/video_video_feed/')
                .then((response) => {
                  if (response.status !== 200) {
                    throw new Error(`Stream request failed with status ${response.status}`);
                  }

                  // 創建新的 Headers 物件並設定回應的 MIME 類型
                  const headers = new Headers(response.headers);
                  headers.append('Content-Type', 'multipart/x-mixed-replace; boundary=frame');

                  // 更新回應的 Headers
                  response.headers = headers;

                  // 處理串流回應
                  handleStreamResponse(response);
                })
                .catch((error) => {
                  console.error('Error:', error);
                });
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
          }
        });
      }
  }

  groupBtn_rightBtn.onclick = () => {
      window.location.reload()
  }
  
});


