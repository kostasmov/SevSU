const pageNames = {
	'index.html' : 'Главная страница',
	'about-me.html' : 'Обо мне',
	'interests.html' : 'Интересы',
	'study.html' : 'Учёба',
	'album.html' : 'Фотоальбом',
	'contacts.html' : 'Контакты',
	'history.html' : 'История просмотра'
}

// Получение значения сookie по его имени 
function getCookie(name) {
	const cookies = document.cookie.split(';')
	for (let cookie of cookies) {
		const [cookieName, cookieValue] = cookie.split('=')
		if (cookieName.trim() === name) {
			return cookieValue
		}
	}
	return ''
}

// Установка cookie с указанным именем
function setCookie(name, value, expirationDays) {
	const d = new Date()
	d.setTime(d.getTime() + expirationDays * 24 * 60 * 60 * 1000)
	const expires = 'expires=' + d.toUTCString()
	document.cookie = name + '=' + value + ';' + expires + ';path=/'
}

// Получение названия страницы из URL
function getPageName(url) {
    const urlParts = url.split('/');
    return urlParts[urlParts.length - 1];
}

// Обновление и отображение истории текущего сеанса
function updateSessionHistory() {
    const sessionHistoryString = sessionStorage.getItem('sessionHistory') || "";
    const sessionHistory = sessionHistoryString ? JSON.parse(sessionHistoryString) : {};
    const sessionTable = document.getElementById('sessionHistory');

    for (let page in sessionHistory) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${getPageName(page)}</td><td>${sessionHistory[page]}</td>`;
        sessionTable.appendChild(row);
    }
}

// Обновление и отображение истории за всё время
function updateAllTimeHistory() {
    const allTimeHistoryString = getCookie('allTimeHistory') || "";
    const allTimeHistory = allTimeHistoryString ? JSON.parse(allTimeHistoryString) : {};
    const allTimeTable = document.getElementById('allTimeHistory');

    for (let page in allTimeHistory) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${getPageName(page)}</td><td>${allTimeHistory[page]}</td>`;
        allTimeTable.appendChild(row);
    }
}

// Добавление страницы в историю просмотра
function addToHistory() {
    const currentPage = window.location.href;
	if ((currentPage.indexOf('#winter') == -1) && 
	(currentPage.indexOf('#spring') == -1) && 
	(currentPage.indexOf('#summer') == -1) &&
	(currentPage.indexOf('#autumn') == -1))
	{
		const sessionHistoryString = sessionStorage.getItem('sessionHistory') || ''
		const sessionHistory = sessionHistoryString
			? JSON.parse(sessionHistoryString)
			: {}
		sessionHistory[getPageName(currentPage)] =
			(sessionHistory[getPageName(currentPage)] || 0) + 1
		sessionStorage.setItem('sessionHistory', JSON.stringify(sessionHistory))

		const allTimeHistoryString = getCookie('allTimeHistory') || ''
		const allTimeHistory = allTimeHistoryString
			? JSON.parse(allTimeHistoryString)
			: {}
		allTimeHistory[getPageName(currentPage)] =
			(allTimeHistory[getPageName(currentPage)] || 0) + 1
		setCookie('allTimeHistory', JSON.stringify(allTimeHistory), 365)
	}
}

// Обновление истории после загрузки страницы
window.onload = function() {
  addToHistory();
  updateSessionHistory();
  updateAllTimeHistory();
};
