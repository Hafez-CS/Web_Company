from rest_framework import serializers
from .models import Transaction
from accounts.serializers import UserSerializer
from tasks_module.serializers import TaskSerializer

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    related_user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'task', 'related_user', 
                  'description', 'created_at']
