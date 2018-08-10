from rest_framework import serializers
from .models import Issue
from django.contrib.auth.models import User

class IssueSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    created_by = serializers.ReadOnlyField(source='created_by.username')
    	

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Issue
        fields = ('title', 'description', 'assigned_to', 'created_by', 'status', 'issue_id')
        read_only_fields = ('issue_id', 'date_created', 'date_modified')