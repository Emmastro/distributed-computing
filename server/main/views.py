from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.http import FileResponse

from .models import Job, Task
from .serializers import JobSerializer, TaskSerializer
from users.models import User


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def get_job_file(self, request, pk=None):
        job = self.get_object()

        file_handle = job.job_file.open()
        response = FileResponse(file_handle, content_type='text/plain')
  
        response['Content-Disposition'] = 'attachment;filename=job.py'

        return response


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    @action(detail=False, methods=['get'])
    def request_task(self, request):
        """attempts to retrieve a new task"""
        # TODO: distribute jobs evenly

        job = Job.objects.filter(status='pending').first()

        if not job:
            return Response({'message': 'no jobs available'})

        user = User.objects.get(pk=request.user.id)
        task = Task.objects.create(
            runner=user, job=job, status='pending')
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        task = self.get_object()
        task.status = 'finished'
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)
