from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Ticket, TicketResponse, TicketAttachment
from .serializers import TicketSerializer, TicketResponseSerializer

class TicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(created_by=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        ticket = serializer.save(created_by=self.request.user)
        
        # Handle file uploads
        files = self.request.FILES.getlist('attachments')
        for file in files:
            TicketAttachment.objects.create(
                ticket=ticket,
                file=file,
                uploaded_by=self.request.user
            )

class TicketDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    
    def get_object(self):
        ticket = super().get_object()
        user = self.request.user
        
        # Only admin or ticket creator can view
        if not (user.is_staff or user == ticket.created_by):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to view this ticket.")
        
        return ticket

class TicketResponseCreateAPIView(generics.CreateAPIView):
    serializer_class = TicketResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        user = self.request.user
        
        # Check permission
        if not (user.is_staff or user == ticket.created_by):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to respond to this ticket.")
        
        is_admin = user.is_staff
        response = serializer.save(ticket=ticket, user=user, is_admin_response=is_admin)
        
        # Update ticket status
        if ticket.status == 'OPEN':
            ticket.status = 'IN_PROGRESS'
            ticket.save()
