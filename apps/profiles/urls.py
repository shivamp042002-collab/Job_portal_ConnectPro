from django.urls import path
from . import views

urlpatterns = [
    path('me/',                          views.MyProfileView.as_view(),      name='my_profile'),
    path('me/experience/',               views.ExperienceView.as_view(),     name='experience'),
    path('me/experience/<int:pk>/',      views.ExperienceView.as_view(),     name='experience_delete'),
    path('me/education/',                views.EducationView.as_view(),      name='education'),
    path('me/education/<int:pk>/',       views.EducationView.as_view(),      name='education_delete'),
    path('<str:username>/',              views.UserProfileView.as_view(),    name='user_profile'),
    path('<str:username>/follow/',       views.FollowToggleView.as_view(),   name='follow_toggle'),
    path('<str:username>/followers/',    views.FollowersListView.as_view(),  name='followers'),
    path('<str:username>/following/',    views.FollowingListView.as_view(),  name='following'),
]