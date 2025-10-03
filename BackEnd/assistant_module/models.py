from django.db import models
from accounts.models import UserProfile

class AssistantConversation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assistant_conversations')
    title = models.CharField(max_length=255, default='New Conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class AssistantMessage(models.Model):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ASSISTANT', 'Assistant'),
    )
    
    conversation = models.ForeignKey(
        AssistantConversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role} - {self.created_at}"
