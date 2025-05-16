from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from task_manager.managers.categories import CategoryManager

User = get_user_model()

status_choices = [
    ("New", "New"),
    ("In Progress", "In Progress"),
    ("Pending", "Pending"),
    ("Blocked", "Blocked"),
    ("Done", "Done")
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CategoryManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]


class Task(models.Model):
    title = models.CharField(max_length=250, unique_for_date="deadline")
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=100, choices=status_choices, default="New")
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [
            models.UniqueConstraint(fields=['title', 'deadline'], name='unique_task_title_per_deadline')
        ]


class SubTask(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=100, choices=status_choices, default="New")
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subtasks'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        constraints = [
            models.UniqueConstraint(fields=['title', 'task'], name='unique_subtask_title_per_task')
        ]