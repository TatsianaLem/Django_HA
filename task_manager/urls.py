from django.urls import path
from task_manager.api_views import (
    TaskCreateAPIView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskStatsView,
    CategoryCreateAPIView,
    SubTaskListCreateAPIView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('categories/create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update'),
]