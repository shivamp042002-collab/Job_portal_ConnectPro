document.addEventListener('DOMContentLoaded', function() {

    var loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            var email    = document.getElementById('email').value.trim();
            var password = document.getElementById('password').value;

            if (!email || !password) {
                showMessage('error-message', 'Please fill in all fields.', 'error');
                return;
            }

            loginBtn.textContent = 'Signing in...';
            loginBtn.disabled    = true;

            apiCall('/api/v1/auth/login/', 'POST', { email: email, password: password },
                function(status, response) {
                    loginBtn.textContent = 'Sign In';
                    loginBtn.disabled    = false;
                    if (status === 200) {
                        saveTokens(response.tokens.access, response.tokens.refresh);
                        showMessage('success-message', 'Login successful! Redirecting...', 'success');
                        setTimeout(function() { window.location.href = '/dashboard/'; }, 1000);
                    } else {
                        showMessage('error-message', response.error || 'Login failed.', 'error');
                    }
                }
            );
        });
    }

    var registerBtn = document.getElementById('register-btn');
    if (registerBtn) {
        registerBtn.addEventListener('click', function() {
            var username  = document.getElementById('username').value.trim();
            var email     = document.getElementById('email').value.trim();
            var password  = document.getElementById('password').value;
            var password2 = document.getElementById('password2').value;

            if (!username || !email || !password || !password2) {
                showMessage('error-message', 'Please fill in all fields.', 'error');
                return;
            }
            if (password !== password2) {
                showMessage('error-message', 'Passwords do not match.', 'error');
                return;
            }

            registerBtn.textContent = 'Creating account...';
            registerBtn.disabled    = true;

            apiCall('/api/v1/auth/register/', 'POST',
                { username:username, email:email, password:password, password2:password2 },
                function(status, response) {
                    registerBtn.textContent = 'Create Account';
                    registerBtn.disabled    = false;
                    if (status === 201) {
                        saveTokens(response.tokens.access, response.tokens.refresh);
                        showMessage('success-message', 'Account created! Redirecting...', 'success');
                        setTimeout(function() { window.location.href = '/dashboard/'; }, 1000);
                    } else {
                        var msg = response.error || response.email && response.email[0]
                                  || response.password && response.password[0]
                                  || 'Registration failed.';
                        showMessage('error-message', msg, 'error');
                    }
                }
            );
        });
    }

});