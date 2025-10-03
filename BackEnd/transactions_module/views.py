from rest_framework import generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        transaction_type = self.request.query_params.get('type')
        
        if user.is_staff:
            queryset = Transaction.objects.all()
        else:
            queryset = Transaction.objects.filter(user=user)
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        return queryset.select_related('user', 'related_user', 'task')

class TaskTransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Transaction.objects.filter(
                transaction_type__in=['TASK_SEND', 'TASK_RECEIVE', 'TASK_COMPLETE']
            )
        
        return Transaction.objects.filter(
            user=user,
            transaction_type__in=['TASK_SEND', 'TASK_RECEIVE', 'TASK_COMPLETE']
        )
