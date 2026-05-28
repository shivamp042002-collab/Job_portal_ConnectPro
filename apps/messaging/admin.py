from django.contrib import admin
from .models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at']
    filter_horizontal = ['participants']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ['sender', 'thread', 'content', 'is_read', 'created_at']
    list_filter   = ['is_read']
    search_fields = ['sender__username', 'content']
    ordering      = ['-created_at']