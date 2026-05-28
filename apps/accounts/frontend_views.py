from django.shortcuts import render


def home(request):
    return render(request, 'accounts/home.html')

def login_page(request):
    return render(request, 'accounts/login.html')

def register_page(request):
    return render(request, 'accounts/register.html')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def profile_page(request, username=None):
    return render(request, 'profiles/profile.html')

def feed_page(request):
    return render(request, 'posts/feed.html')

def inbox_page(request):
    return render(request, 'messaging/inbox.html')