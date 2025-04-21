from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from task_manager.models import Task
from django.db.models import Count
from task_manager.serializers import TaskSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

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
