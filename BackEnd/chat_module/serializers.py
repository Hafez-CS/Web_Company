from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "username", "text", "created_at"]
