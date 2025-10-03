from rest_framework import serializers
from .models import Ticket, TicketResponse, TicketAttachment
from accounts.serializers import UserSerializer

class TicketAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TicketAttachment
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']

class TicketResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TicketResponse
        fields = ['id', 'ticket', 'user', 'text', 'is_admin_response', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    responses = TicketResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'created_by', 'status', 
                  'priority', 'created_at', 'updated_at', 'attachments', 'responses']
