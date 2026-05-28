function getAccessToken()  { return localStorage.getItem('access_token'); }
function getRefreshToken() { return localStorage.getItem('refresh_token'); }

function saveTokens(access, refresh) {
    localStorage.setItem('access_token',  access);
    localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

function showMessage(elementId, message, type) {
    var el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.className   = 'alert alert-' + type;
    el.style.display = 'block';
    setTimeout(function() { el.style.display = 'none'; }, 5000);
}

function apiCall(url, method, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var token = getAccessToken();
    if (token) { xhr.setRequestHeader('Authorization', 'Bearer ' + token); }
    xhr.onload = function() {
        var response;
        try { response = JSON.parse(xhr.responseText); }
        catch(e) { response = {}; }
        callback(xhr.status, response);
    };
    xhr.onerror = function() { callback(0, { error: 'Network error.' }); };
    xhr.send(data ? JSON.stringify(data) : null);
}

function togglePassword(fieldId) {
    var input = document.getElementById(fieldId);
    input.type = input.type === 'password' ? 'text' : 'password';
}

document.addEventListener('DOMContentLoaded', function() {
    var token    = getAccessToken();
    var navLinks = document.getElementById('nav-links');
    if (!navLinks) return;

    if (token) {
        navLinks.innerHTML =
            '<a href="/feed/">Feed</a>' +
            '<a href="/profile/">Profile</a>' +
            '<a href="/messages/">Messages</a>' +
            '<a href="/dashboard/">Dashboard</a>' +
            '<a href="#" id="logout-link">Logout</a>';

        document.getElementById('logout-link').addEventListener('click', function(e) {
            e.preventDefault();
            apiCall('/api/v1/auth/logout/', 'POST', { refresh: getRefreshToken() },
                function() { clearTokens(); window.location.href = '/'; }
            );
        });
    }
});