document.addEventListener('DOMContentLoaded', function() {
    var token = getAccessToken();
    if (!token) { window.location.href = '/login/'; return; }

    var parts    = window.location.pathname.split('/').filter(Boolean);
    var username = (parts[0] === 'profile' && parts[1]) ? parts[1] : null;
    var apiUrl   = username ? '/api/v1/profiles/' + username + '/' : '/api/v1/profiles/me/';
    var isOwnProfile = !username;

    apiCall(apiUrl, 'GET', null, function(status, data) {
        if (status !== 200) { alert('Profile not found.'); return; }

        document.getElementById('profile-name').textContent     = data.username;
        document.getElementById('profile-headline').textContent = data.headline || '';
        document.querySelector('#profile-location span').textContent = data.location || '';
        document.getElementById('profile-bio').textContent      = data.bio || 'No bio added yet.';
        document.getElementById('followers-count').textContent  = data.followers_count;
        document.getElementById('following-count').textContent  = data.following_count;
        document.getElementById('profile-avatar').textContent   = data.username.charAt(0).toUpperCase();

        var skillsEl = document.getElementById('profile-skills');
        skillsEl.innerHTML = data.skills_list && data.skills_list.length
            ? data.skills_list.map(function(s) {
                return '<span class="skill-tag">' + s + '</span>';
              }).join('')
            : '<p style="color:var(--text-light)">No skills listed yet.</p>';

        var expEl = document.getElementById('profile-experience');
        expEl.innerHTML = data.experiences && data.experiences.length
            ? data.experiences.map(function(e) {
                return '<div class="experience-item">' +
                    '<h4>' + e.title + '</h4>' +
                    '<p>' + e.company + (e.location ? ' · ' + e.location : '') + '</p>' +
                    '<p class="date-range">' + e.start_date + ' → ' + (e.is_current ? 'Present' : (e.end_date || '')) + '</p>' +
                    (e.description ? '<p>' + e.description + '</p>' : '') +
                    '</div>';
              }).join('')
            : '<p style="color:var(--text-light)">No experience listed yet.</p>';

        var eduEl = document.getElementById('profile-education');
        eduEl.innerHTML = data.education && data.education.length
            ? data.education.map(function(e) {
                return '<div class="experience-item">' +
                    '<h4>' + e.degree + '</h4>' +
                    '<p>' + e.school + (e.field_of_study ? ' · ' + e.field_of_study : '') + '</p>' +
                    '<p class="date-range">' + e.start_year + ' — ' + (e.end_year || 'Present') + '</p>' +
                    '</div>';
              }).join('')
            : '<p style="color:var(--text-light)">No education listed yet.</p>';

        var followBtn = document.getElementById('follow-btn');
        var editBtn   = document.getElementById('edit-btn');

        if (isOwnProfile) {
            editBtn.style.display = 'inline-flex';
        } else {
            followBtn.style.display   = 'inline-flex';
            followBtn.textContent     = data.is_following ? 'Unfollow' : 'Follow';
            followBtn.className       = data.is_following ? 'btn btn-outline' : 'btn btn-primary';
            followBtn.addEventListener('click', function() {
                apiCall('/api/v1/profiles/' + data.username + '/follow/', 'POST', null,
                    function(s, res) {
                        if (s === 200 || s === 201) {
                            var following = res.is_following;
                            followBtn.textContent = following ? 'Unfollow' : 'Follow';
                            followBtn.className   = following ? 'btn btn-outline' : 'btn btn-primary';
                            var cnt = parseInt(document.getElementById('followers-count').textContent);
                            document.getElementById('followers-count').textContent = following ? cnt + 1 : cnt - 1;
                        }
                    }
                );
            });
        }
    });
});