var currentThreadId = null;
var pollInterval    = null;

document.addEventListener('DOMContentLoaded', function() {
    var token = getAccessToken();
    if (!token) { window.location.href = '/login/'; return; }
    loadThreads();
});

// ── Load all threads ──────────────────────────────────────
function loadThreads() {
    apiCall('/api/v1/messages/', 'GET', null, function(status, data) {
        var list = document.getElementById('thread-list');
        if (status !== 200) {
            list.innerHTML = '<p class="empty-state">Could not load messages.</p>';
            return;
        }
        if (!data.results && !data.length) {
            list.innerHTML = '<p class="empty-state">No messages yet.<br>Start a new conversation!</p>';
            return;
        }
        var threads = data.results || data;
        if (!threads.length) {
            list.innerHTML = '<p class="empty-state">No messages yet.<br>Start a new conversation!</p>';
            return;
        }
        list.innerHTML = threads.map(function(t) {
            return renderThreadItem(t);
        }).join('');
    });
}

function renderThreadItem(t) {
    return '<div class="thread-item" id="thread-item-' + t.id + '" onclick="openThread(' + t.id + ', \'' + t.other_user + '\')">' +
        '<div class="thread-avatar">' + t.other_user.charAt(0).toUpperCase() + '</div>' +
        '<div class="thread-info">' +
            '<div class="thread-name">' + t.other_user +
                (t.unread_count > 0 ? ' <span class="unread-badge">' + t.unread_count + '</span>' : '') +
            '</div>' +
            '<div class="thread-preview">' + (t.last_message || 'No messages yet') + '</div>' +
        '</div>' +
    '</div>';
}

// ── Open a thread ─────────────────────────────────────────
function openThread(threadId, otherUser) {
    currentThreadId = threadId;

    // Highlight selected thread
    document.querySelectorAll('.thread-item').forEach(function(el) {
        el.classList.remove('active');
    });
    var item = document.getElementById('thread-item-' + threadId);
    if (item) item.classList.add('active');

    var main = document.getElementById('inbox-main');
    main.innerHTML =
        '<div class="message-header">' +
            '<div class="thread-avatar">' + otherUser.charAt(0).toUpperCase() + '</div>' +
            '<div><strong>' + otherUser + '</strong></div>' +
        '</div>' +
        '<div class="message-list" id="message-list"><div class="loading-spinner">Loading...</div></div>' +
        '<div class="message-input-area">' +
            '<input type="text" id="message-input" placeholder="Type a message..." ' +
                   'onkeydown="if(event.key===\'Enter\') sendMessage()">' +
            '<button class="btn btn-primary" onclick="sendMessage()">Send</button>' +
        '</div>';

    loadMessages(threadId);

    // Poll for new messages every 5 seconds
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(function() {
        loadMessages(threadId);
    }, 5000);
}

// ── Load messages in a thread ─────────────────────────────
function loadMessages(threadId) {
    apiCall('/api/v1/messages/' + threadId + '/messages/', 'GET', null,
        function(status, data) {
            var list = document.getElementById('message-list');
            if (!list) return;
            if (status !== 200) {
                list.innerHTML = '<p class="empty-state">Could not load messages.</p>';
                return;
            }
            var messages = data.results || data;
            if (!messages.length) {
                list.innerHTML = '<p class="empty-state">No messages yet. Say hello! 👋</p>';
                return;
            }
            list.innerHTML = messages.map(function(m) {
                return renderMessage(m);
            }).join('');

            // Scroll to bottom
            list.scrollTop = list.scrollHeight;

            // Remove unread badge
            var badge = document.querySelector('#thread-item-' + threadId + ' .unread-badge');
            if (badge) badge.remove();
        }
    );
}

function renderMessage(m) {
    return '<div class="message-bubble ' + (m.is_mine ? 'mine' : 'theirs') + '">' +
        '<div class="bubble-content">' + escapeHtml(m.content) + '</div>' +
        '<div class="bubble-time">' + formatTime(m.created_at) +
            (m.is_mine ? (m.is_read ? ' ✓✓' : ' ✓') : '') +
        '</div>' +
    '</div>';
}

// ── Send a message ────────────────────────────────────────
function sendMessage() {
    if (!currentThreadId) return;
    var input   = document.getElementById('message-input');
    var content = input.value.trim();
    if (!content) return;

    input.value    = '';
    input.disabled = true;

    apiCall(
        '/api/v1/messages/' + currentThreadId + '/messages/send/',
        'POST',
        { content: content },
        function(status, data) {
            input.disabled = false;
            input.focus();
            if (status === 201) {
                loadMessages(currentThreadId);
                loadThreads();
            }
        }
    );
}

// ── Start new thread ──────────────────────────────────────
function showNewMessage() {
    var username = prompt('Enter username to message:');
    if (!username || !username.trim()) return;

    apiCall('/api/v1/messages/start/', 'POST',
        { username: username.trim() },
        function(status, data) {
            if (status === 200 || status === 201) {
                loadThreads();
                setTimeout(function() {
                    openThread(data.id, data.other_user);
                }, 300);
            } else {
                alert(data.error || 'User not found.');
            }
        }
    );
}

// ── Utilities ─────────────────────────────────────────────
function escapeHtml(text) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(text));
    return d.innerHTML;
}

function formatTime(dateStr) {
    if (!dateStr) return '';
    var date = new Date(dateStr);
    var now  = new Date();
    var diff = Math.floor((now - date) / 1000);
    if (diff < 60)    return 'just now';
    if (diff < 3600)  return Math.floor(diff / 60) + 'm ago';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h ago';
    return date.toLocaleDateString();
}