<script>
    document.addEventListener("DOMContentLoaded", function() {
        // Focus on the first input of the form when the page loads
        if (document.querySelector('.form-container .sign-up input[name="username"]:focus') === null) {
            document.querySelector('.form-container .sign-up input[name="username"]').focus();
        }

        // Get the container and buttons
        const container = document.getElementById('container');
        const registerBtn = document.getElementById('register');
        const loginBtn = document.getElementById('login');

        // When the Register button is clicked, add the 'active' class to the container
        registerBtn.addEventListener('click', () => {
            container.classList.add("active");
        });

        // When the Login button is clicked, remove the 'active' class from the container
        loginBtn.addEventListener('click', () => {
            container.classList.remove("active");
        });
    });
</script>
