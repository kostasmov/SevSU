$(document).ready(function() {
  var openModalButton = $("#openModalButton");
  var $modal = $('#modal');
  var $confirmBtn = $('#confirmBtn');
  var $cancelBtn = $('#cancelBtn');

  openModalButton.click(function() {
    $("#overlay").fadeIn();
    $modal.fadeIn();
  });

  // Открыть модальное окно при отправке формы
  $('#contactForm').submit(function(event) {
    event.preventDefault();
      
    $("#overlay").fadeIn();
    $modal.fadeIn();
  });

  // Закрыть модальное окно
  function closeModal() {
    $("#overlay").fadeOut();
    $modal.fadeOut();
  }

  // Подтвердить отправку формы
  $confirmBtn.click(function() {
    closeModal();
    $('#contactForm').off('submit').submit();
  });

  // Отменить отправку формы
  $cancelBtn.click(function() {
    closeModal();
  });
});