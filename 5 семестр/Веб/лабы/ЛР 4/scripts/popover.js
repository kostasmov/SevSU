// Функция для отображения Popover
function showPopover(element, message) {
  var popover = $('#popover');
  popover.html(message);
  popover.css({
    display: 'block',
    left: (element.offsetLeft + element.offsetWidth) + 10 + 'px',
    top: element.offsetTop - 10  + 'px'
  });
  setTimeout(hidePopover, 5000);
}
  
// Функция для скрытия Popover
function hidePopover() {
  var popover = $('#popover');
  popover.css('display', 'none');
}

// Обработчики событий
$(document).ready(function() {
  $('#full_name').mouseover(function() {
    showPopover(this, '* Введите ваше полное имя');
  });

  $('#full_name').mouseout(function() {
    hidePopover();
  });

  $('#birthday').mouseover(function() {
    showPopover(this, '* Введите вашу дату рождения');
  });

  $('#birthday').mouseout(function() {
    hidePopover();
  });

  $('#phone').mouseover(function() {
    showPopover(this, '* Введите ваш телефон');
  });

  $('#phone').mouseout(function() {
    hidePopover();
  });

  $('#mail').mouseover(function() {
    showPopover(this, '* Введите вашу почту');
  });

  $('#mail').mouseout(function() {
    hidePopover();
  });

  $('#message').mouseover(function() {
    showPopover(this, '* Введите ваше сообщение');
  });

  $('#message').mouseout(function() {
    hidePopover();
  });

  $('#quest3').mouseover(function() {
    showPopover(this, '* Сам думай!');
  });

  $('#quest3').mouseout(function() {
    hidePopover();
  });
});