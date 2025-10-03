from django.db import models
from accounts.models import UserProfile
from tasks_module.models import Task

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('TASK_SEND', 'Task Send'),
        ('TASK_RECEIVE', 'Task Receive'),
        ('TASK_COMPLETE', 'Task Complete'),
        ('MESSAGE_SEND', 'Message Send'),
        ('MESSAGE_RECEIVE', 'Message Receive'),
    )
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    related_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='related_transactions'
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.created_at}"
