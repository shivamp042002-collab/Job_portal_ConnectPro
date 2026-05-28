from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer

User = get_user_model()


class ThreadListView(generics.ListAPIView):
    """List all threads for the logged-in user."""
    serializer_class   = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Thread.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')

    def get_serializer_context(self):
        return {'request': self.request}


class StartThreadView(APIView):
    """
    Start a new thread with another user.
    If thread already exists, return the existing one.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username', '').strip()
        if not username:
            return Response(
                {'error': 'Username is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        target = get_object_or_404(User, username=username)

        if target == request.user:
            return Response(
                {'error': 'You cannot message yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if thread already exists between these two users
        existing = Thread.objects.filter(
            participants=request.user
        ).filter(
            participants=target
        ).first()

        if existing:
            serializer = ThreadSerializer(
                existing, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new thread
        thread = Thread.objects.create()
        thread.participants.add(request.user, target)

        serializer = ThreadSerializer(thread, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageListView(generics.ListAPIView):
    """
    List all messages in a thread.
    Also marks all messages as read.
    """
    serializer_class   = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        thread = get_object_or_404(
            Thread,
            id=self.kwargs['thread_id'],
            participants=self.request.user
        )
        # Mark unread messages as read
        thread.messages.filter(
            is_read=False
        ).exclude(
            sender=self.request.user
        ).update(is_read=True)

        return thread.messages.select_related('sender')

    def get_serializer_context(self):
        return {'request': self.request}


from apps.accounts.throttles import MessageRateThrottle

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes   = [MessageRateThrottle]

    def post(self, request, thread_id):
        thread = get_object_or_404(
            Thread,
            id=thread_id,
            participants=request.user
        )
        content = request.data.get('content', '').strip()
        if not content:
            return Response(
                {'error': 'Message content is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = Message.objects.create(
            thread=thread,
            sender=request.user,
            content=content
        )

        # Update thread timestamp so it floats to top
        thread.save()

        serializer = MessageSerializer(
            message, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteMessageView(APIView):
    """Delete your own message."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, thread_id, message_id):
        thread = get_object_or_404(
            Thread,
            id=thread_id,
            participants=request.user
        )
        message = get_object_or_404(
            Message,
            id=message_id,
            thread=thread
        )

        if message.sender != request.user:
            return Response(
                {'error': 'You can only delete your own messages.'},
                status=status.HTTP_403_FORBIDDEN
            )

        message.delete()
        return Response(
            {'message': 'Message deleted.'},
            status=status.HTTP_200_OK
        )


class UnreadCountView(APIView):
    """Get total unread message count for navbar badge."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Message.objects.filter(
            thread__participants=request.user,
            is_read=False
        ).exclude(
            sender=request.user
        ).count()
        return Response({'unread_count': count})