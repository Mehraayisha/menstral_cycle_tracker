<<<<<<< HEAD
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
=======


>>>>>>> f32bd92cfc6077859dc08c4ff7a190e565812d08

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

<<<<<<< HEAD
loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
=======
        // When the Register button is clicked, add the 'active' class to the container
        registerBtn.addEventListener('click', () => {
            container.classList.add("active");
        });

        // When the Login button is clicked, remove the 'active' class from the container
        loginBtn.addEventListener('click', () => {
            container.classList.remove("active");
        });
   
>>>>>>> f32bd92cfc6077859dc08c4ff7a190e565812d08
