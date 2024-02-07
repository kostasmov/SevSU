var currentPageUrl = window.location.href;
var links = document.querySelectorAll('nav li a');

// Переход по наведению для ссылок на другие страницы
// links.forEach((link) => {
//   if (link.href == currentPageUrl || link.href.indexOf('interests.html') != -1) {
//     return;
//   }

//   link.addEventListener('mouseover', () => {
//     link.click();
//   });
// });