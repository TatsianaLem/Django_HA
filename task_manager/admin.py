from django.contrib import admin
from task_manager.models import Category, Task, SubTask


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'categories')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)
    filter_horizontal = ('categories',)
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return (obj.title[:10] + '...') if len(obj.title) > 10 else obj.title

    short_title.short_description = 'Название'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)
    actions = ['mark_done']

    @admin.action(description='Пометить как done')
    def mark_done(self, request, queryset):
        updated = queryset.update(status='Done')
        self.message_user(request, f"Обновлено {updated} подзадач до статуса 'Done'")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

