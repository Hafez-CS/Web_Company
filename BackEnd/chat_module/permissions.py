from rest_framework import permissions
from groups_module.models import ChatRoomParticipant

class IsChatRoomParticipant(permissions.BasePermission):
    """
    Check if user is an active participant of the chatroom
    """
    def has_object_permission(self, request, view, obj):
        # obj can be Message or ChatRoom
        room = obj if hasattr(obj, 'room_type') else obj.room
        
        return ChatRoomParticipant.objects.filter(
            chatroom=room,
            user=request.user,
            is_active=True
        ).exists()
