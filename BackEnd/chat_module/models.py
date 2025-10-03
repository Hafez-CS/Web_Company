from django.db import models
from accounts.models import UserProfile
from groups_module.models import ChatRoom

class Message(models.Model):
    MESSAGE_TYPES = (
        ('USER', 'User'),
        ('SYSTEM', 'System'),
        ('ASSISTANT', 'Assistant'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="messages")
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='message_attachments/')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for message {self.message.id}"

class MessageReaction(models.Model):
    REACTION_TYPES = (
        ('LIKE', '👍'),
        ('LOVE', '❤️'),
        ('LAUGH', '😂'),
        ('WOW', '😮'),
        ('SAD', '😢'),
        ('ANGRY', '😠'),
    )
    
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.reaction_type}"

class MessageReadStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'user')
    
    def __str__(self):
        return f"{self.user.username} read message {self.message.id}"