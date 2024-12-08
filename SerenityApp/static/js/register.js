document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const name = document.getElementById('id_name').value; // Note the 'id_' prefix added by Django forms
        const department = document.getElementById('id_department').value;
        const priority = document.getElementById('id_priority').value;

        fetch('/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // Include CSRF token for security
            },
            body: JSON.stringify({
                name: name,
                department: department,
                priority: priority
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Registration successful!');
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
