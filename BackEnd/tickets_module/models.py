from django.db import models
from accounts.models import UserProfile

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    )
    
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )
    
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject} - {self.created_by.username}"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    is_admin_response = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.ticket.subject}"

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='ticket_attachments/')
    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
