from django.urls import path
from .views import TransactionListAPIView, TaskTransactionListAPIView

urlpatterns = [
    path('transactions/', TransactionListAPIView.as_view(), name='transaction-list'),
    path('transactions/tasks/', TaskTransactionListAPIView.as_view(), name='task-transaction-list'),
]
