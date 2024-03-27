$(document).ready(function () {
  let languageSelect = document.querySelectorAll('.language-select a')
  languageSelect.forEach((el) => {
      el.addEventListener('click', () => {
          if (el.classList.contains('language-en')) {
              $('.alert-date-h').text('h');
              $('.alert-date-m').text('m');
              $('.alert-date-s').text('s');
          } else {
              $('.alert-date-h').text('時');
              $('.alert-date-m').text('分');
              $('.alert-date-s').text('秒');
          }
      })
  })

  if (localStorage.getItem('language') === 'zh') {
    $('.alert-date-h').text('時');
    $('.alert-date-m').text('分');
    $('.alert-date-s').text('秒');
    };

  $(`.${localStorage.getItem('alert')}`).addClass('active');

  $('.page-link').click(function () { 
    localStorage.removeItem('alert')
  });

  let alertSearch = document.querySelectorAll('.content-cum');
  alertSearch.forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault()
      if (el.getAttribute('data-is-deleted') == 'yes'){
        Swal.fire({
          icon: 'error',
          title: localStorage.getItem('language') === 'zh'
                  ? '已刪除'
                  : 'Already delete',
          color: '#fff',
          background: 'cadetblue',
      });
      return
      }
      $.ajax({
        type: "GET",
        url: "/auth/alert_check_date_quantity_ajax",
        data: {
          item: el.getAttribute('data-item'),
          item_id: el.getAttribute('data-item-id'),
          date: el.getAttribute('data-date'),
        },
        success: function (response) {
          if (response.ok === 'success') {
            let alertIndex = response.alert_index;
            let item = el.getAttribute('data-item');

            if (alertIndex <= 14) {
              if (item === 'image') {
                var path = window.location.origin + `/image/photo/${el.getAttribute('data-date')}`;
              } else if (item === 'video') {
                var path = window.location.origin + `/video/album_video/${el.getAttribute('data-date')}`;
              } else if (item === 'folder') {
                var path = window.location.origin + `/image/image_multiple_folder/${el.getAttribute('data-date')}`;
              }  
            } else {
              let page = Math.ceil(alertIndex / 14);
              if (item === 'image') {
                var path = window.location.origin + `/image/photo/${el.getAttribute('data-date')}/?page=${page}`;
              } else if (item === 'video') {
                var path = window.location.origin + `/video/album_video/${el.getAttribute('data-date')}/?page=${page}`;
              } else if (item === 'folder') {
                var path = window.location.origin + `/image/image_multiple_folder/${el.getAttribute('data-date')}/?page=${page}}`;
              }  
            }
            localStorage.setItem('item_animation', `item${el.getAttribute('data-item-id')}`);
            window.location.href = path;
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
  accordion.init({ speed: 300, oneOpen: true });
});

var accordion = (function(){
    var $accordion = $('.js-accordion');
    var $accordion_header = $accordion.find('.js-accordion-header');
    var $accordion_item = $('.js-accordion-item');
   
    // default settings 
    var settings = {
      // animation speed
      speed: 400,
      
      // close all other accordion items if true
      oneOpen: false
    };
      
    return {
      // pass configurable object literal
      init: function($settings) {
        $accordion_header.on('click', function() {
          accordion.toggle($(this));
        });
        
        $.extend(settings, $settings); 
        
        // ensure only one accordion is active if oneOpen is true
        if(settings.oneOpen && $('.js-accordion-item.active').length > 1) {
          $('.js-accordion-item.active:not(:first)').removeClass('active');
        }
        
        // reveal the active accordion bodies
        $('.js-accordion-item.active').find('> .js-accordion-body').show();
      },
      toggle: function($this) {
              
        if(settings.oneOpen && $this[0] != $this.closest('.js-accordion').find('> .js-accordion-item.active > .js-accordion-header')[0]) {
          $this.closest('.js-accordion')
                 .find('> .js-accordion-item') 
                 .removeClass('active')
                 .find('.js-accordion-body')
                 .slideUp()
        }
        
        // show/hide the clicked accordion item
        $this.closest('.js-accordion-item').toggleClass('active');
        $this.next().stop().slideToggle(settings.speed);
      }
    }
  })();

