document.getElementById('submitButton').addEventListener('click', function(event) {
    event.preventDefault();

    var nameInput = document.getElementById('nameInput');
    var emailInput = document.getElementById('emailInput');
    var subjectInput = document.getElementById('subjectInput');
    var messageInput = document.getElementById('messageInput');
    
    if (nameInput.value.trim() === '') {
        nameInput.style.borderColor = 'red';
    }else{
        nameInput.style.borderColor = '';
    }

    if (emailInput.value.trim() === '') {
        emailInput.style.borderColor = 'red';
    }else{
        emailInput.style.borderColor = '';
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailInput.value.trim())) {
        emailInput.style.borderColor = 'red';
    }else{
        emailInput.style.borderColor = '';
    }

    if (subjectInput.value.trim() === '') {
        subjectInput.style.borderColor = 'red';
    }else{
        subjectInput.style.borderColor = '';
    }

    if (messageInput.value.trim() === '') {
        messageInput.style.borderColor = 'red';
    }else{
        messageInput.style.borderColor = '';
    }

    if(messageInput.value.trim() === ''||subjectInput.value.trim() === ''||!emailRegex.test(emailInput.value.trim())||emailInput.value.trim() === ''||nameInput.value.trim() === ''){
        return;
    }else{
    alert('Message sent successfully!');
    setTimeout(function() {
        location.reload();
    }, 100);
    }
}); 
