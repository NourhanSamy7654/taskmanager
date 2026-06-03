from rest_framework import serializers
from tasks.models import Task

class TaskSellizer(serializers.ModelSerializer):

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description',
            'status', 'status_display',
            'priority', 'priority_display',
            'due_date', 'created_at', 'updated_at',
            'owner', 'owner_username',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']
  