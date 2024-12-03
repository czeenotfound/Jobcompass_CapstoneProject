const togglePassword = document.getElementById('toggle-password');
const toggleConfirmPassword = document.getElementById('toggle-confirm-password');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');

// Add toggle functionality for password field
togglePassword.addEventListener('click', () => {
    const icon = togglePassword.querySelector('i');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.className = 'fa-solid fa-eye'; // Switch to eye icon
    } else {
        passwordInput.type = 'password';
        icon.className = 'fa-solid fa-eye-slash'; // Switch to eye-slash icon
    }
});

// Add toggle functionality for confirm password field
toggleConfirmPassword.addEventListener('click', () => {
    const icon = toggleConfirmPassword.querySelector('i');
    if (confirmPasswordInput.type === 'password') {
        confirmPasswordInput.type = 'text';
        icon.className = 'fa-solid fa-eye'; // Switch to eye icon
    } else {
        confirmPasswordInput.type = 'password';
        icon.className = 'fa-solid fa-eye-slash'; // Switch to eye-slash icon
    }
});