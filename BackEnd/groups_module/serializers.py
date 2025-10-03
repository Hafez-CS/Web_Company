from rest_framework import serializers
from .models import Group, GroupMembership, ChatRoom, ChatRoomParticipant
from accounts.serializers import UserSerializer

class GroupMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'user_id', 'role', 'joined_at', 'is_active']

class GroupSerializer(serializers.ModelSerializer):
    supervisor = UserSerializer(read_only=True)
    supervisor_id = serializers.IntegerField(write_only=True, required=False)
    memberships = GroupMembershipSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'supervisor', 'supervisor_id', 
                  'memberships', 'created_by', 'created_at', 'is_active']

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'group', 'participants', 'created_at', 'is_active']
    
    def get_participants(self, obj):
        participants = obj.participants.filter(is_active=True)
        return [{'id': p.user.id, 'username': p.user.username, 'email': p.user.email} 
                for p in participants]
