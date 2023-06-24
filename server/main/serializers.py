from rest_framework import serializers
from users.models import User

from .models import Job, Task


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'name', 'description',
                  'job_file', 'nbr_tasks', 'created_at', 'status')
        read_only_fields = ('id', 'created_at')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'job', 'status', 'result', 'started_at', 'finished_at')
        read_only_fields = ('id', 'created_at', 'task_id',)
