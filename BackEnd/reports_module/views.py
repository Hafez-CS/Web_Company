from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Report
from .serializers import ReportSerializer
from tasks_module.models import Task
from groups_module.models import Group, GroupMembership
from groups_module.permissions import IsAdminUser

class TaskSummaryReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get date range from query params
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)
        
        if user.is_staff:
            tasks = Task.objects.filter(created_at__gte=start_date)
        else:
            tasks = Task.objects.filter(assigned_to=user, created_at__gte=start_date)
        
        # Task statistics
        data = {
            'total_tasks': tasks.count(),
            'pending_tasks': tasks.filter(status='PENDING').count(),
            'in_progress_tasks': tasks.filter(status='IN_PROGRESS').count(),
            'completed_tasks': tasks.filter(status='COMPLETED').count(),
            'rejected_tasks': tasks.filter(status='REJECTED').count(),
            'tasks_by_priority': {
                'low': tasks.filter(priority='LOW').count(),
                'medium': tasks.filter(priority='MEDIUM').count(),
                'high': tasks.filter(priority='HIGH').count(),
            },
            'tasks_by_status_over_time': self._get_tasks_over_time(tasks, days)
        }
        
        return Response({
            'success': True,
            'data': data
        })
    
    def _get_tasks_over_time(self, tasks, days):
        result = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            day_tasks = tasks.filter(created_at__date=date.date())
            result.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': day_tasks.count(),
                'completed': day_tasks.filter(status='COMPLETED').count()
            })
        return list(reversed(result))

class UserActivityReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)
        
        # Get all users with their task counts
        from accounts.models import UserProfile
        users_data = []
        
        for user in UserProfile.objects.filter(is_active=True):
            assigned_tasks = Task.objects.filter(
                assigned_to=user,
                created_at__gte=start_date
            )
            
            users_data.append({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'total_tasks': assigned_tasks.count(),
                'completed_tasks': assigned_tasks.filter(status='COMPLETED').count(),
                'pending_tasks': assigned_tasks.filter(status='PENDING').count(),
                'completion_rate': self._calculate_completion_rate(assigned_tasks)
            })
        
        return Response({
            'success': True,
            'data': {
                'users': users_data,
                'period_days': days
            }
        })
    
    def _calculate_completion_rate(self, tasks):
        total = tasks.count()
        if total == 0:
            return 0
        completed = tasks.filter(status='COMPLETED').count()
        return round((completed / total) * 100, 2)

class GroupPerformanceReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        groups = Group.objects.filter(is_active=True)
        groups_data = []
        
        for group in groups:
            members = GroupMembership.objects.filter(group=group, is_active=True)
            member_ids = members.values_list('user_id', flat=True)
            
            group_tasks = Task.objects.filter(assigned_to__id__in=member_ids)
            
            groups_data.append({
                'group_id': group.id,
                'group_name': group.name,
                'supervisor': group.supervisor.username if group.supervisor else None,
                'total_members': members.count(),
                'total_tasks': group_tasks.count(),
                'completed_tasks': group_tasks.filter(status='COMPLETED').count(),
                'pending_tasks': group_tasks.filter(status='PENDING').count(),
                'completion_rate': self._calculate_completion_rate(group_tasks)
            })
        
        return Response({
            'success': True,
            'data': {
                'groups': groups_data
            }
        })
    
    def _calculate_completion_rate(self, tasks):
        total = tasks.count()
        if total == 0:
            return 0
        completed = tasks.filter(status='COMPLETED').count()
        return round((completed / total) * 100, 2)

class SaveReportAPIView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

class ReportListAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = Report.objects.all().order_by('-created_at')
