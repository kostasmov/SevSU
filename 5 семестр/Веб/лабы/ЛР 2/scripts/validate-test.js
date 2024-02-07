function validateForm(event, nameInput, messageInput) {
    if (!validateName(nameInput.value)) {
        event.preventDefault();
        alert("Ошибка: Неверно введено ФИО");
        nameInput.focus();
        nameInput.classList.add("red-border");
        return;
    }
  
    if (!validateMessage(messageInput.value)) {
        event.preventDefault();
        alert("Ошибка: В ответе менее 20 слов");
        messageInput.focus();
        messageInput.classList.add("red-border");
        return;
    }
}

function validateName(name) {
    var namePattern = /^[а-яА-Я]+\s[а-яА-Я]+\s[а-яА-Я]+$/;
    return namePattern.test(name);
}
  
function validateMessage(textarea) {
    var words = textarea.trim().split(" ");
    return words.length >= 20
  }