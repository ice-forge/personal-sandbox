document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const messages = document.querySelectorAll('.error-message, .success-message');

        messages.forEach(message => {
            message.style.transition = 'opacity 0.5s ease-out';
            message.style.opacity = '0';

            setTimeout(function() {
                message.remove();
            }, 500);
        });
    }, 5000);
});
