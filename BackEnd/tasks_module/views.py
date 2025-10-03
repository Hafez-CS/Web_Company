from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Task, TaskAttachment, TaskResponse, TaskResponseAttachment
from .serializers import TaskSerializer, TaskResponseSerializer
from groups_module.permissions import IsAdminUser
from accounts.models import UserProfile

class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all().order_by('-created_at')
        return Task.objects.filter(assigned_to=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response(
                {"detail": "Only admin can create tasks."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        task = serializer.save(created_by=self.request.user)
        
        # Handle file uploads
        files = self.request.FILES.getlist('attachments')
        for file in files:
            TaskAttachment.objects.create(
                task=task,
                file=file,
                uploaded_by=self.request.user
            )

class TaskDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        
        # Only admin or assigned user can update
        if not (request.user.is_staff or request.user == task.assigned_to):
            return Response(
                {"detail": "You don't have permission to update this task."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)

class TaskRejectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        rejection_reason = request.data.get('rejection_reason')
        
        if not rejection_reason:
            return Response(
                {"detail": "Rejection reason is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = 'REJECTED'
        task.rejection_reason = rejection_reason
        task.save()
        
        return Response(
            {"detail": "Task rejected successfully.", "task": TaskSerializer(task).data},
            status=status.HTTP_200_OK
        )

class TaskResponseCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        
        if task.assigned_to != self.request.user:
            return Response(
                {"detail": "You can only respond to your own tasks."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        response = serializer.save(task=task, user=self.request.user)
        
        # Handle file uploads
        files = self.request.FILES.getlist('attachments')
        for file in files:
            TaskResponseAttachment.objects.create(response=response, file=file)
        
        # Update task status
        task.status = 'IN_PROGRESS'
        task.save()

class MyTasksAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status')
        
        queryset = Task.objects.filter(assigned_to=user)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
