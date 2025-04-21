from django.urls import path
from task_manager.api_views import (
    TaskCreateAPIView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskStatsView,
)

urlpatterns = [
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
]