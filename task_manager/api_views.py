from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from task_manager.models import Task, Category, SubTask
from django.db.models import Count
from task_manager.serializers import (
    TaskSerializer,
    CategoryCreateSerializer,
    TaskCreateSerializer,
    SubTaskCreateSerializer
)
from task_manager.pagination import SubTaskPagination
from django.utils import timezone
from django.shortcuts import get_object_or_404

class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data)

class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(data=serializer.data)

class TaskListByWeekdayAPIView(APIView):
    def get_queryset(self, request):
        tasks = Task.objects.all()

        weekday_param = request.query_params.get('weekday')

        if weekday_param:
            weekdays = {
                'понедельник': 0,
                'вторник': 1,
                'среда': 2,
                'четверг': 3,
                'пятница': 4,
                'суббота': 5,
                'воскресенье': 6,
            }
            weekday_num = weekdays.get(weekday_param.lower())
            if weekday_num is not None:
                tasks = tasks.filter(deadline__week_day=weekday_num + 1)
        return tasks

    def get(self, request):
        queryset = self.get_queryset(request=request)

        serializer = TaskSerializer(queryset, many=True)
        return Response(data=serializer.data)

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

class CategoryCreateAPIView(APIView):
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskListCreateAPIView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()

        if not subtasks.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(data=serializer.data)

    def put(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubTaskPaginatedListAPIView(ListAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

class SubTaskFilteredListAPIView(ListAPIView):
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')

        task_title = self.request.query_params.get('task_title')
        status_param = self.request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset