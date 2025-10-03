from django.urls import path
from .views import (
    TaskListCreateAPIView,
    TaskDetailAPIView,
    TaskRejectAPIView,
    TaskResponseCreateAPIView,
    MyTasksAPIView
)

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tasks/<int:id>/reject/', TaskRejectAPIView.as_view(), name='task-reject'),
    path('tasks/<int:id>/responses/', TaskResponseCreateAPIView.as_view(), name='task-response-create'),
    path('my-tasks/', MyTasksAPIView.as_view(), name='my-tasks'),
]
