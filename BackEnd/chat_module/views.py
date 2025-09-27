from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer

# Create your views here.

class MessageListAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
