from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Message, MessageAttachment, MessageReaction, MessageReadStatus
from .serializers import (
    MessageSerializer, 
    MessageReactionSerializer,
    MessageReadStatusSerializer
)
from groups_module.models import ChatRoom, ChatRoomParticipant
from transactions_module.models import Transaction

class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        room = get_object_or_404(ChatRoom, id=room_id)
        
        # Check if user is participant
        if not ChatRoomParticipant.objects.filter(
            chatroom=room, 
            user=self.request.user, 
            is_active=True
        ).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a member of this chatroom.")
        
        # Get messages, excluding soft-deleted ones
        messages = room.messages.filter(is_deleted=False).select_related('user')
        
        # Mark messages as read
        unread_messages = messages.exclude(
            read_statuses__user=self.request.user
        )
        for message in unread_messages:
            MessageReadStatus.objects.get_or_create(
                message=message,
                user=self.request.user
            )
        
        return messages.order_by('created_at')  # Oldest first for chat

class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room_id = self.request.data.get("room_id")
        if not room_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"room_id": "This field is required."})

        room = get_object_or_404(ChatRoom, id=room_id)

        # Check membership
        if not ChatRoomParticipant.objects.filter(
            chatroom=room, 
            user=self.request.user, 
            is_active=True
        ).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a member of this chatroom.")

        message = serializer.save(user=self.request.user, room=room)
        
        # Handle file uploads
        files = self.request.FILES.getlist('attachments')
        for file in files:
            MessageAttachment.objects.create(
                message=message,
                file=file,
                file_name=file.name,
                file_size=file.size
            )
        
        # Create transaction record
        other_participants = ChatRoomParticipant.objects.filter(
            chatroom=room,
            is_active=True
        ).exclude(user=self.request.user)
        
        for participant in other_participants:
            Transaction.objects.create(
                user=self.request.user,
                transaction_type='MESSAGE_SEND',
                related_user=participant.user,
                description=f"Message sent in {room.name}"
            )
            Transaction.objects.create(
                user=participant.user,
                transaction_type='MESSAGE_RECEIVE',
                related_user=self.request.user,
                description=f"Message received in {room.name}"
            )

class MessageUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        room_id = self.kwargs.get("room_id")
        message_id = self.kwargs.get("message_id")
        return get_object_or_404(Message, id=message_id, room_id=room_id)

    def perform_update(self, serializer):
        message = self.get_object()
        
        # Only message owner can edit
        if message.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own messages.")
        
        serializer.save(is_edited=True)

    def perform_destroy(self, instance):
        # Check permissions: owner or admin/room manager
        user = self.request.user
        room = instance.room
        
        is_owner = instance.user == user
        is_admin = user.is_staff
        
        # Check if user is room manager (for group rooms)
        from groups_module.models import GroupMembership
        is_manager = False
        if room.group:
            is_manager = GroupMembership.objects.filter(
                group=room.group,
                user=user,
                role__in=['SUPERVISOR'],
                is_active=True
            ).exists()
        
        if not (is_owner or is_admin or is_manager):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to delete this message.")
        
        # Soft delete
        instance.is_deleted = True
        instance.save()

class MessageReactionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        reaction_type = request.data.get('reaction_type')
        
        if not reaction_type:
            return Response(
                {"detail": "reaction_type is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is participant
        if not ChatRoomParticipant.objects.filter(
            chatroom=message.room,
            user=request.user,
            is_active=True
        ).exists():
            return Response(
                {"detail": "You are not a member of this chatroom."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Toggle reaction
        reaction, created = MessageReaction.objects.get_or_create(
            message=message,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )
        
        if not created:
            if reaction.reaction_type == reaction_type:
                # Remove reaction if same type
                reaction.delete()
                return Response(
                    {"detail": "Reaction removed."},
                    status=status.HTTP_200_OK
                )
            else:
                # Update reaction type
                reaction.reaction_type = reaction_type
                reaction.save()
        
        return Response(
            MessageReactionSerializer(reaction).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

class UnreadMessageCountAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get all chatrooms user is part of
        chatrooms = ChatRoom.objects.filter(
            participants__user=user,
            participants__is_active=True
        )
        
        unread_counts = []
        total_unread = 0
        
        for room in chatrooms:
            unread = Message.objects.filter(
                room=room,
                is_deleted=False
            ).exclude(
                Q(user=user) | Q(read_statuses__user=user)
            ).count()
            
            if unread > 0:
                unread_counts.append({
                    'room_id': room.id,
                    'room_name': room.name,
                    'room_type': room.room_type,
                    'unread_count': unread
                })
                total_unread += unread
        
        return Response({
            'success': True,
            'data': {
                'total_unread': total_unread,
                'rooms': unread_counts
            }
        })

class SearchMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('q', '')
        room_id = self.request.query_params.get('room_id')
        
        # Get rooms user has access to
        accessible_rooms = ChatRoom.objects.filter(
            participants__user=user,
            participants__is_active=True
        )
        
        queryset = Message.objects.filter(
            room__in=accessible_rooms,
            is_deleted=False,
            text__icontains=query
        )
        
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        
        return queryset.order_by('-created_at')
