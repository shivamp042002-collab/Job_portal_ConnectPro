from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth import get_user_model
from apps.core.validators import validate_message_content

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source='sender.username', read_only=True
    )
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model  = Message
        fields = [
            'id', 'sender_username', 'content',
            'is_read', 'is_mine', 'created_at'
        ]
        read_only_fields = [
            'id', 'sender_username', 'is_read',
            'is_mine', 'created_at'
        ]

    def get_is_mine(self, obj):
        request = self.context.get('request')
        return obj.sender == request.user if request else False

    def validate_content(self, value):
        validate_message_content(value)
        return value


class ThreadSerializer(serializers.ModelSerializer):
    other_user        = serializers.SerializerMethodField()
    last_message      = serializers.SerializerMethodField()
    last_message_time = serializers.SerializerMethodField()
    unread_count      = serializers.SerializerMethodField()

    class Meta:
        model  = Thread
        fields = [
            'id', 'other_user', 'last_message',
            'last_message_time', 'unread_count', 'updated_at'
        ]

    def get_other_user(self, obj):
        request = self.context.get('request')
        if request:
            other = obj.get_other_user(request.user)
            return other.username if other else None
        return None

    def get_last_message(self, obj):
        msg = obj.last_message()
        return msg.content[:60] if msg else None

    def get_last_message_time(self, obj):
        msg = obj.last_message()
        return msg.created_at if msg else None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(
                is_read=False
            ).exclude(sender=request.user).count()
        return 0