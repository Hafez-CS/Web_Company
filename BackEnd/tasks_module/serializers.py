from rest_framework import serializers
from .models import Task, TaskAttachment, TaskResponse, TaskResponseAttachment
from accounts.serializers import UserSerializer

class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskAttachment
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']

class TaskResponseAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResponseAttachment
        fields = ['id', 'file', 'uploaded_at']

class TaskResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    attachments = TaskResponseAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = TaskResponse
        fields = ['id', 'task', 'user', 'text', 'attachments', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    responses = TaskResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_by', 'assigned_to', 
                  'assigned_to_id', 'group', 'status', 'priority', 'due_date',
                  'created_at', 'updated_at', 'rejection_reason', 'attachments', 'responses']
