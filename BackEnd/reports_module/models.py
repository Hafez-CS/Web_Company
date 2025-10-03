from django.db import models
from accounts.models import UserProfile

class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('TASK_SUMMARY', 'Task Summary'),
        ('USER_ACTIVITY', 'User Activity'),
        ('GROUP_PERFORMANCE', 'Group Performance'),
    )
    
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    generated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.created_at}"
