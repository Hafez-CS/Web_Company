from rest_framework import serializers
from .models import AssistantConversation, AssistantMessage

class AssistantMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantMessage
        fields = ['id', 'role', 'content', 'created_at']

class AssistantConversationSerializer(serializers.ModelSerializer):
    messages = AssistantMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = AssistantConversation
        fields = ['id', 'title', 'messages', 'created_at', 'updated_at', 'is_active']
