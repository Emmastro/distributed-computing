from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required

from .models import Job, Task
from .serializers import JobSerializer, TaskSerializer
from users.models import User


class ApiEndpoint(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, *args, **kwargs):
        print("user", request.user)
        #help(request)
        return HttpResponse(f'Hello, OAuth2! {request.user}')

@login_required()
def secret_page(request, *args, **kwargs):
    print(request, request.user)
    return HttpResponse(f'Secret contents!', status=200)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [TokenHasReadWriteScope]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        job = self.get_object()
        tasks = Task.objects.filter(job=job)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TokenHasReadWriteScope]


    @action(detail=False, methods=['get'])
    def request_task(self, request):
        """attempts to retrieve a new task"""
        # TODO: distribute jobs evenly
        job = Job.objects.filter(status='pending').first()

        if not job:
            return Response({'message': 'no jobs available'})
        
        print("user", request.user)

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
