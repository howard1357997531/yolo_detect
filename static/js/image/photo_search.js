$(document).ready(function () {
  let item = localStorage.getItem('item_animation')
  $(`.${item}`).addClass('item_animation');

  $(`.${item}`).hover(function () {
      $(this).removeClass('item_animation');
      localStorage.removeItem('item_animation')
    }, function () {
      // out
    }
  );
});


