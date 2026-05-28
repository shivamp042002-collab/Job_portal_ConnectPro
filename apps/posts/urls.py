from django.urls import path
from . import views

urlpatterns = [
    # Feed — GET (list) + POST (create)
    path('',
         views.FeedView.as_view(),
         name='feed'),

    path('create/',
         views.PostCreateView.as_view(),
         name='post_create'),

    # Single post — GET, PUT, DELETE
    path('<int:pk>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    # Like toggle
    path('<int:pk>/like/',
         views.LikeToggleView.as_view(),
         name='post_like'),

    # Comments
    path('<int:pk>/comments/',
         views.CommentListCreateView.as_view(),
         name='post_comments'),

    path('<int:pk>/comments/<int:comment_pk>/',
         views.CommentDeleteView.as_view(),
         name='comment_delete'),

    # All posts by a user
    path('user/<str:username>/',
         views.UserPostsView.as_view(),
         name='user_posts'),
]