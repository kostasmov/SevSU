function validateForm(event, nameInput, phoneInput) {  
    if (!validateName(nameInput.value)) {
        event.preventDefault();
        alert("Ошибка: Неверно введено ФИО");
        nameInput.focus();
        nameInput.classList.add("red-border");
        return;
    }
    
    if (!validatePhone(phoneInput.value)) {
        event.preventDefault();
        alert("Ошибка: Неверно введён номер телефона");
        phoneInput.focus();
        phoneInput.classList.add("red-border");
        return;
    }
}

function validateName(name) {
    var namePattern = /^[а-яА-Я]+\s[а-яА-Я]+\s[а-яА-Я]+$/;
    return namePattern.test(name);
}
  
function validatePhone(phone) {
    var phonePattern = /^(\+7|\+3)\d{9,11}$/;
    return phonePattern.test(phone);
}