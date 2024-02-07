
const form = document.getElementById('contactForm');
const submitButton = document.getElementById('submit');

validateForm();

// Проверка наличия заполнения поля
function validateRequiredField(field) {
  return field.value.trim() != "";
}
  
// Проверка корректности ввода имени
function validateName(name) {
  var namePattern = /^[а-яА-Я]+\s[а-яА-Я]+\s[а-яА-Я]+$/;
  return namePattern.test(name);
}

// Проверка корректности ввода номера телефона
function validatePhone(phone) {
  var phonePattern = /^(\+7|\+3)\d{9,11}$/;
  return phonePattern.test(phone);
}

// Скрыть сообщение об ошибке
function hideError(errorElement) {
  errorElement.style.display = "none";
}

// Отобразить сообщение об ошибке
function showError(errorElement, errorMessage) {
  errorElement.textContent = errorMessage;
  errorElement.style.display = "block";
  errorElement.style.color = "red";
}

// Проверка корректности заполнения поля
function validateField(field) {
  var errorElement = document.getElementById(field.id + "-error");

  if (!validateRequiredField(field)) {
    field.classList.remove("valid-input");
    field.classList.add("error-input");
    showError(errorElement, "Поле не может быть пустым");
  } 
  else if (field.id == "full_name" && !validateName(field.value)) {
    field.classList.remove("valid-input");
    field.classList.add("error-input");
    showError(errorElement, "Введите полное имя (Фамилия Имя Отчество)");
  } 
  else if (field.id == "phone" && !validatePhone(field.value)) {
    field.classList.remove("valid-input");
    field.classList.add("error-input");
    showError(errorElement, "Введите корректный номер телефона");
  } 
  else if (field.id == "mail" && !field.validity.valid) {
    field.classList.remove("valid-input");
    field.classList.add("error-input");
    showError(errorElement, "Введите корректный адрес почты");
  } 
  else {
    field.classList.remove("error-input");
    field.classList.add("valid-input");
    hideError(errorElement);
  }

  validateForm();
}

// Функция для проверки корректности заполнения всей формы
function validateForm() {
  var fullNameInput = document.getElementById("full_name");
  var birthdayInput = document.getElementById("birthday");
  var emailInput = document.getElementById("mail");
  var phoneInput = document.getElementById("phone");
  var messageInput = document.getElementById("message");
  var genderInput = document.querySelector('input[name="sex"]:checked');
  var ageSelect = document.getElementById("age");

  var isFullNameValid = validateRequiredField(fullNameInput) && validateName(fullNameInput.value);
  var isBirthdayValid = validateRequiredField(birthdayInput);
  var isEmailValid = validateRequiredField(emailInput) && emailInput.validity.valid;
  var isPhoneValid = validateRequiredField(phoneInput) && validatePhone(phoneInput.value);
  var isMessageValid = validateRequiredField(messageInput);
  var isGenderValid = (genderInput != null);
  var isAgeValid = validateRequiredField(ageSelect);

  if (isFullNameValid && isBirthdayValid && isEmailValid && isPhoneValid && isMessageValid && isGenderValid && isAgeValid) {
    submitButton.disabled = false;
  } else {
    submitButton.disabled = true;
  }
}

// Проверка заполнения формы при снятии фокуса с её полей
document.getElementById("full_name").addEventListener("blur", function() {
  validateField(this);
});

document.getElementById("birthday").addEventListener("blur", function() {
  validateField(this);
});

document.getElementById("mail").addEventListener("blur", function() {
  validateField(this);
});

document.getElementById("phone").addEventListener("blur", function() {
  validateField(this);
});

document.getElementById("message").addEventListener("blur", function() {
  validateField(this);
});

// Особые случаи (пол, возраст)
document.querySelectorAll('input[name="sex"]').forEach(function(radio) {
  radio.addEventListener("change", function() {
    validateForm(this);
  });
});

document.getElementById("age").addEventListener("change", function() {
  validateField(this);
});

document.getElementById("age").addEventListener("blur", function() {
  validateField(this);
});