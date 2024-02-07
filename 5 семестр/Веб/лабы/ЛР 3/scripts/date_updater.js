var monthNames = [
  "января", "февраля", "марта", "апреля", "мая", "июня",
  "июля", "августа", "сентября", "октября", "ноября", "декабря"
];

// Обновление даты и времени в навигационной панели
function updateDateTime() {
  var now = new Date();

  var hours = now.getHours();
  var minutes = now.getMinutes();
  var seconds = now.getSeconds();
  var day = now.getDate();
  var month = monthNames[now.getMonth()];
  var year = now.getFullYear();

  var dateTimeString = hours + ':' + ('0' + minutes).slice(-2) + ':';
  dateTimeString += ('0' + seconds).slice(-2) + ' ' + day + ' ' + month + ' ' + year;

  var dateTimeElement = document.getElementById('currentDateTime');
  if (dateTimeElement) {
      dateTimeElement.textContent = dateTimeString;
  }
}