from django.urls import path
from rest_framework.routers import DefaultRouter
from task_manager.api_views import (
    RegisterAPIView,
    MyTaskListAPIView,
    # TaskCreateAPIView,
    # TaskListAPIView,
    # TaskDetailAPIView,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDeleteAPIView,
    TaskStatsView,
    #CategoryCreateAPIView,
    CategoryViewSet,
    SubTaskListCreateAPIView,
    # SubTaskDetailUpdateDeleteView,
    SubTaskRetrieveUpdateDeleteAPIView,
    TaskListByWeekdayAPIView,
    SubTaskPaginatedListAPIView,
    SubTaskFilteredListAPIView,
    LogoutAPIView,
)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),

    path('tasks/my/', MyTaskListAPIView.as_view(), name='my-tasks'),
    # path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    # path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    # path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDeleteAPIView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),

    #path('categories/create/', CategoryCreateAPIView.as_view(), name='category-create'),

    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    # path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDeleteAPIView.as_view(), name='subtask-detail'),
    path('tasks/by-weekday/', TaskListByWeekdayAPIView.as_view(), name='task-by-weekday'),
    path('subtasks/paginated/', SubTaskPaginatedListAPIView.as_view(), name='subtask-paginated'),
    path('subtasks/filtered/', SubTaskFilteredListAPIView.as_view(), name='subtask-filtered'),
] + router.urls