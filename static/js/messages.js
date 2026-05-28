document.addEventListener('DOMContentLoaded', function() {
    var token = getAccessToken();
    if (!token) { window.location.href = '/login/'; return; }
    loadThreads();
});

function loadThreads() {
    apiCall('/api/v1/messages/', 'GET', null, function(status, data) {
        var list = document.getElementById('thread-list');
        if (status !== 200 || !data.length) {
            list.innerHTML = '<p class="empty-state">No messages yet.</p>';
            return;
        }
        list.innerHTML = data.map(function(thread) {
            return '<div class="thread-item" onclick="openThread(' + thread.id + ')">' +
                '<div class="thread-avatar">' + thread.other_user.charAt(0).toUpperCase() + '</div>' +
                '<div class="thread-info">' +
                    '<div class="thread-name">' + thread.other_user + '</div>' +
                    '<div class="thread-preview">' + (thread.last_message || '') + '</div>' +
                '</div>' +
            '</div>';
        }).join('');
    });
}

function showNewMessage() {
    var username = prompt('Enter username to message:');
    if (!username) return;
    apiCall('/api/v1/messages/start/', 'POST', { username: username }, function(status, data) {
        if (status === 200 || status === 201) { loadThreads(); }
        else { alert('User not found.'); }
    });
}

function openThread(threadId) {
    document.getElementById('message-area').innerHTML =
        '<p class="empty-state">Messages coming in Phase 4...</p>';
}