from django.db import models
from accounts.models import UserProfile

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    supervisor = models.ForeignKey(
        UserProfile, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='supervised_groups'
    )
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='created_groups'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class GroupMembership(models.Model):
    ROLE_CHOICES = (
        ('SUPERVISOR', 'Supervisor'),
        ('MEMBER', 'Member'),
    )
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'group')

class ChatRoom(models.Model):
    ROOM_TYPE_CHOICES = (
        ('GROUP', 'Group Chat'),
        ('PRIVATE', 'Private Chat'),
    )
    
    name = models.CharField(max_length=255)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='chatrooms',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.room_type})"

class ChatRoomParticipant(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='chatroom_participants')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('chatroom', 'user')
