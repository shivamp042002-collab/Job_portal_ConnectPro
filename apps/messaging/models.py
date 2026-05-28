from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Thread(models.Model):
    """
    A conversation thread between exactly two users.
    """
    participants = models.ManyToManyField(User, related_name='threads')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'threads'
        ordering = ['-updated_at']

    def __str__(self):
        users = self.participants.all()
        return f"Thread: {' & '.join([u.username for u in users])}"

    def get_other_user(self, current_user):
        return self.participants.exclude(id=current_user.id).first()

    def last_message(self):
        return self.messages.order_by('-created_at').first()


class Message(models.Model):
    thread     = models.ForeignKey(Thread,  on_delete=models.CASCADE, related_name='messages')
    sender     = models.ForeignKey(User,    on_delete=models.CASCADE, related_name='sent_messages')
    content    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:40]}"