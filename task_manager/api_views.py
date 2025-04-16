from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from task_manager.models import Task
from django.db.models import Count
from task_manager.serializers import TaskSerializer
from django.utils import timezone


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailAPIView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskStatsView(APIView):
    def get(self, request):
        today = timezone.now().date()

        total_tasks = Task.objects.count()
        tasks_by_status = Task.objects.values('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=today).count()

        return Response({
            'total_tasks': total_tasks,
            'tasks_by_status': tasks_by_status,
            'overdue_tasks': overdue_tasks
        })
