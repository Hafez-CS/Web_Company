from django.urls import path
from .views import (
    TaskSummaryReportAPIView,
    UserActivityReportAPIView,
    GroupPerformanceReportAPIView,
    SaveReportAPIView,
    ReportListAPIView
)

urlpatterns = [
    path('reports/task-summary/', TaskSummaryReportAPIView.as_view(), name='task-summary-report'),
    path('reports/user-activity/', UserActivityReportAPIView.as_view(), name='user-activity-report'),
    path('reports/group-performance/', GroupPerformanceReportAPIView.as_view(), name='group-performance-report'),
    path('reports/save/', SaveReportAPIView.as_view(), name='save-report'),
    path('reports/', ReportListAPIView.as_view(), name='report-list'),
]
