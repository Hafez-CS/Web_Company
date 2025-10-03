from rest_framework import serializers
from .models import Report
from accounts.serializers import UserSerializer

class ReportSerializer(serializers.ModelSerializer):
    generated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'name', 'report_type', 'generated_by', 'data', 'created_at']
