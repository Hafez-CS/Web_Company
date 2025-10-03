from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Group, GroupMembership, ChatRoom, ChatRoomParticipant
from .serializers import GroupSerializer, GroupMembershipSerializer, ChatRoomSerializer
from .permissions import IsAdminUser, IsGroupSupervisorOrAdmin
from accounts.models import UserProfile

class GroupListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return Group.objects.filter(is_active=True).prefetch_related('memberships__user')
    
    @transaction.atomic
    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        
        # Create group chatroom
        group_chatroom = ChatRoom.objects.create(
            name=f"{group.name} - Group Chat",
            room_type='GROUP',
            group=group
        )
        
        # Add supervisor if exists
        if group.supervisor:
            GroupMembership.objects.create(
                user=group.supervisor,
                group=group,
                role='SUPERVISOR'
            )
            ChatRoomParticipant.objects.create(
                chatroom=group_chatroom,
                user=group.supervisor
            )

class GroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = Group.objects.all()
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class GroupMembershipListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = GroupMembershipSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return GroupMembership.objects.filter(group_id=group_id, is_active=True)
    
    @transaction.atomic
    def perform_create(self, serializer):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        user_id = self.request.data.get('user_id')
        user = get_object_or_404(UserProfile, id=user_id)
        
        membership = serializer.save(group=group, user=user)
        
        # Add to group chatroom
        group_chatroom = group.chatrooms.filter(room_type='GROUP').first()
        if group_chatroom:
            ChatRoomParticipant.objects.get_or_create(
                chatroom=group_chatroom,
                user=user
            )
        
        # Create private chatrooms with supervisor and admin
        supervisor = group.supervisor
        if supervisor and supervisor != user:
            private_room_name = f"Private: {supervisor.username} - {user.username}"
            private_room, created = ChatRoom.objects.get_or_create(
                name=private_room_name,
                room_type='PRIVATE',
                group=group
            )
            if created:
                ChatRoomParticipant.objects.create(chatroom=private_room, user=supervisor)
                ChatRoomParticipant.objects.create(chatroom=private_room, user=user)

class GroupMembershipDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupMembershipSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get_object(self):
        group_id = self.kwargs.get('group_id')
        membership_id = self.kwargs.get('membership_id')
        return get_object_or_404(GroupMembership, id=membership_id, group_id=group_id)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class UserChatRoomsAPIView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            participants__user=user,
            participants__is_active=True,
            is_active=True
        ).distinct()
