from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import AssistantConversation, AssistantMessage
from .serializers import AssistantConversationSerializer, AssistantMessageSerializer
import random

class AssistantConversationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AssistantConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AssistantConversation.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-updated_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AssistantConversationDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = AssistantConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AssistantConversation.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class AssistantChatAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, conversation_id):
        conversation = get_object_or_404(
            AssistantConversation,
            id=conversation_id,
            user=request.user
        )
        
        user_message = request.data.get('message')
        
        if not user_message:
            return Response({
                'success': False,
                'detail': 'Message is required.'
            }, status=400)
        
        # Save user message
        AssistantMessage.objects.create(
            conversation=conversation,
            role='USER',
            content=user_message
        )
        
        # Generate mock AI response
        ai_response = self._generate_mock_response(user_message)
        
        # Save assistant message
        assistant_message = AssistantMessage.objects.create(
            conversation=conversation,
            role='ASSISTANT',
            content=ai_response
        )
        
        conversation.save()  # Update timestamp
        
        return Response({
            'success': True,
            'data': {
                'user_message': user_message,
                'assistant_message': AssistantMessageSerializer(assistant_message).data
            }
        })
    
    def _generate_mock_response(self, user_message):
        """Mock AI response - replace with actual AI integration later"""
        responses = [
            "I understand your question. Let me help you with that.",
            "That's an interesting point. Here's what I think...",
            "Based on your request, I would recommend...",
            "I can assist you with that. Let me provide some guidance.",
            "Thank you for your question. Here's my response..."
        ]
        
        # Simple keyword-based mock responses
        if 'task' in user_message.lower():
            return "I can help you manage your tasks. You can create, view, and update tasks through the tasks module."
        elif 'report' in user_message.lower():
            return "I can generate various reports for you including task summaries, user activity, and group performance metrics."
        elif 'ticket' in user_message.lower():
            return "You can create support tickets and track their status. Admin will respond to your tickets."
        else:
            return random.choice(responses)
