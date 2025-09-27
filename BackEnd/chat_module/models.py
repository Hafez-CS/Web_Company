from django.db import models
from accounts.models import UserProfile

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"
