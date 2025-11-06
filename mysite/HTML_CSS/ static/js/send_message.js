document.addEventListener("DOMContentLoaded", function() {
    var container = document.querySelector('.popup-container');
    var popupButtons = document.querySelectorAll('.open-popup');

    popupButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            container.style.display = 'flex';
        });
    });

    container.addEventListener('click', function(event) {
        if (event.target === container) {
            container.style.display = 'none';
        }
    });

    var sendBtn = container.querySelector('.send-btn');
    sendBtn.addEventListener('click', function() {
        container.style.display = 'none';
    });
});
