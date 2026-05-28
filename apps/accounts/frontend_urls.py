from django.urls import path
from . import frontend_views

urlpatterns = [
    path('',                          frontend_views.home,         name='home'),
    path('login/',                    frontend_views.login_page,   name='login_page'),
    path('register/',                 frontend_views.register_page,name='register_page'),
    path('dashboard/',                frontend_views.dashboard,    name='dashboard'),
    path('profile/',                  frontend_views.profile_page, name='profile_page'),
    path('profile/<str:username>/',   frontend_views.profile_page, name='user_profile_page'),
    path('feed/',                     frontend_views.feed_page,    name='feed_page'),
    path('messages/',                 frontend_views.inbox_page,   name='inbox_page'),
]