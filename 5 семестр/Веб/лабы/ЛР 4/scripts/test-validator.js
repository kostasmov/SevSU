function checkTestForm() {
    form = document.getElementById("testForm");
    form.addEventListener('submit', function(event) {
        var nameInput = document.getElementById('full_name');
        var answerInput = document.getElementById('quest3');

        nameInput.classList.remove("red-border"); 
        answerInput.classList.remove("red-border");

        if (!nameInput.value || !answerInput.value) {
            event.preventDefault();
            alert('Пожалуйста, заполните все поля формы.');

            if (!nameInput.value) {
                nameInput.focus();
                nameInput.classList.add("red-border");
                return;
            } else {
                answerInput.focus();
                answerInput.classList.add("red-border");
                return;
            }
        }

        validateForm(event, nameInput, answerInput);
        return;
    });
}

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