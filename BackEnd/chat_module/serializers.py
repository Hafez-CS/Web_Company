from rest_framework import serializers
from .models import Message, MessageAttachment, MessageReaction, MessageReadStatus
from accounts.serializers import UserSerializer

class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file', 'file_name', 'file_size', 'uploaded_at']

class MessageReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MessageReaction
        fields = ['id', 'user', 'reaction_type', 'created_at']

class MessageReadStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MessageReadStatus
        fields = ['id', 'user', 'read_at']

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user = UserSerializer(read_only=True)
    room_id = serializers.IntegerField(write_only=True)
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    reactions = MessageReactionSerializer(many=True, read_only=True)
    read_by = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id", "user", "username", "room", "room_id", "text", 
            "message_type", "created_at", "updated_at", "is_deleted", 
            "is_edited", "attachments", "reactions", "read_by", "reaction_count"
        ]
        read_only_fields = ['room', 'user', 'created_at', 'updated_at', 'is_edited']
    
    def get_read_by(self, obj):
        return obj.read_statuses.count()
    
    def get_reaction_count(self, obj):
        from django.db.models import Count
        reaction_counts = obj.reactions.values('reaction_type').annotate(count=Count('id'))
        return {item['reaction_type']: item['count'] for item in reaction_counts}
