document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const institution_id = document.getElementById('institution_id').value;
    const errorMsg = document.getElementById('errorMsg');
    const loginBtn = document.getElementById('loginBtn');

    errorMsg.classList.add('hidden');
    loginBtn.disabled = true;
    loginBtn.innerText = 'Signing in...';

    try {
        const result = await API.login(email, password, institution_id);
        console.log("Login Result:", result);

        if (result.status === 'success') {
            localStorage.setItem('user', JSON.stringify(result.user));
            if (result.user.role === 'admin') {
                window.location.href = 'dashboard.html';
            } else {
                window.location.href = 'feedback.html';
            }
        } else {
            console.error("Login Error:", result.message);
            errorMsg.innerText = result.message || "Invalid credentials. Please try again.";
            errorMsg.classList.remove('hidden');
        }
    } catch (error) {
        console.error("Exception during login:", error);
        errorMsg.innerText = "An unexpected error occurred. Please check your connection.";
        errorMsg.classList.remove('hidden');
    }

    loginBtn.disabled = false;
    loginBtn.innerText = 'Sign In';
});
