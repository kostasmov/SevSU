function checkContactForm() {
    form = document.getElementById("contactForm");
    form.addEventListener('submit', function(event) {
        var nameInput = document.getElementById('full_name');
        var emailInput = document.getElementById('mail');
        var phoneInput = document.getElementById('phone');
        var messageInput = document.getElementById('message');

        nameInput.classList.remove("red-border"); 
        emailInput.classList.remove("red-border"); 
        phoneInput.classList.remove("red-border"); 
        messageInput.classList.remove("red-border"); 

        if (!nameInput.value || !messageInput.value || !phoneInput.value || !emailInput.value) {
            event.preventDefault();
            alert('Пожалуйста, заполните все поля формы.');
    
            if (!nameInput.value) {
              nameInput.focus();
              nameInput.classList.add("red-border");
              return;
            } else if (!phoneInput.value) {
                phoneInput.focus();
                phoneInput.classList.add("red-border");
                return;
            } else if (!emailInput.value) {
              emailInput.focus();
              emailInput.classList.add("red-border");
              return;
            } else {
              messageInput.focus();
              messageInput.classList.add("red-border");
              return;
            }
        }
        
        validateForm(event, nameInput, phoneInput);
        return;
  });
}

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