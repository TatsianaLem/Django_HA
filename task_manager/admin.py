from django.contrib import admin
from task_manager.models import Category, Task, SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'categories')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)
    filter_horizontal = ('categories',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

