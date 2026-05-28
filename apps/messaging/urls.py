from django.urls import path
from . import views

urlpatterns = [
    # All threads
    path('',
         views.ThreadListView.as_view(),
         name='thread_list'),

    # Start new thread
    path('start/',
         views.StartThreadView.as_view(),
         name='start_thread'),

    # Unread count badge
    path('unread/',
         views.UnreadCountView.as_view(),
         name='unread_count'),

    # Messages inside a thread
    path('<int:thread_id>/messages/',
         views.MessageListView.as_view(),
         name='message_list'),

    # Send message
    path('<int:thread_id>/messages/send/',
         views.SendMessageView.as_view(),
         name='send_message'),

    # Delete message
    path('<int:thread_id>/messages/<int:message_id>/delete/',
         views.DeleteMessageView.as_view(),
         name='delete_message'),
]