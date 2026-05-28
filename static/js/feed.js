document.addEventListener('DOMContentLoaded', function() {
    var token = getAccessToken();
    if (!token) { window.location.href = '/login/'; return; }

    loadFeed();
    setupPostSubmit();

    apiCall('/api/v1/auth/me/', 'GET', null, function(status, data) {
        if (status === 200) {
            document.getElementById('feed-avatar').textContent = data.username.charAt(0).toUpperCase();
        }
    });
});

function loadFeed() {
    apiCall('/api/v1/posts/', 'GET', null, function(status, data) {
        var feedList = document.getElementById('feed-list');
        if (status !== 200) {
            feedList.innerHTML = '<p class="empty-feed">Could not load feed.</p>';
            return;
        }
        var posts = data.results || data;
        if (!posts.length) {
            feedList.innerHTML = '<div class="empty-feed"><p style="font-size:2rem">📰</p><p>No posts yet. Be the first to post!</p></div>';
            return;
        }
        feedList.innerHTML = posts.map(function(post) {
            return renderPost(post);
        }).join('');
    });
}

function renderPost(post) {
    return '<div class="post-card" id="post-' + post.id + '">' +
        '<div class="post-header">' +
            '<div class="post-avatar">' + (post.author_username || 'U').charAt(0).toUpperCase() + '</div>' +
            '<div>' +
                '<div class="post-user-name">' + (post.author_username || 'Unknown') + '</div>' +
                '<div class="post-time">' + formatTime(post.created_at) + '</div>' +
            '</div>' +
        '</div>' +
        '<div class="post-content">' + post.content + '</div>' +
        '<div class="post-actions">' +
            '<button class="post-action-btn ' + (post.is_liked ? 'liked' : '') + '" onclick="toggleLike(' + post.id + ', this)">👍 ' + (post.likes_count || 0) + '</button>' +
            '<button class="post-action-btn">💬 ' + (post.comments_count || 0) + ' Comments</button>' +
        '</div>' +
    '</div>';
}

function toggleLike(postId, btn) {
    apiCall('/api/v1/posts/' + postId + '/like/', 'POST', null, function(status, res) {
        if (status === 200 || status === 201) {
            btn.textContent = '👍 ' + res.likes_count;
            btn.className   = 'post-action-btn ' + (res.is_liked ? 'liked' : '');
        }
    });
}

function setupPostSubmit() {
    var submitBtn = document.getElementById('submit-post');
    if (!submitBtn) return;
    submitBtn.addEventListener('click', function() {
        var content = document.getElementById('post-content').value.trim();
        if (!content) return;
        submitBtn.textContent = 'Posting...';
        submitBtn.disabled    = true;
        apiCall('/api/v1/posts/', 'POST', { content: content }, function(status, data) {
            submitBtn.textContent = 'Post';
            submitBtn.disabled    = false;
            if (status === 201) {
                document.getElementById('post-content').value    = '';
                document.getElementById('post-form').style.display = 'none';
                loadFeed();
            }
        });
    });
}

function formatTime(dateStr) {
    if (!dateStr) return '';
    var date  = new Date(dateStr);
    var now   = new Date();
    var diff  = Math.floor((now - date) / 1000);
    if (diff < 60)   return 'just now';
    if (diff < 3600) return Math.floor(diff / 60) + 'm ago';
    if (diff < 86400)return Math.floor(diff / 3600) + 'h ago';
    return Math.floor(diff / 86400) + 'd ago';
}