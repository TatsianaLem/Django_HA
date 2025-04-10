import os
import sys
import django
from datetime import timedelta, date


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_proj.settings")
django.setup()

from task_manager.models import Task, SubTask

def create_records():
    task = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status="New",
        deadline=date.today() + timedelta(days=3)
    )

    SubTask.objects.create(
        title="Gather information",
        description="Find necessary information for the presentation",
        status="New",
        deadline=date.today() + timedelta(days=2),
        task=task
    )

    SubTask.objects.create(
        title="Create slides",
        description="Create presentation slides",
        status="New",
        deadline=date.today() + timedelta(days=1),
        task=task
    )
    print("Задача и подзадачи созданы.")


def read_records():
    print("\n Задачи со статусом 'New':")
    for task in Task.objects.filter(status="New"):
        print(f"- {task.title}")

    print("\n Подзадачи со статусом 'Done' и просроченным дедлайном:")
    for subtask in SubTask.objects.filter(status="Done", deadline__lt=date.today()):
        print(f"- {subtask.title} (дедлайн: {subtask.deadline})")


def update_records():
    try:
        task = Task.objects.get(title="Prepare presentation")
        task.status = "In progress"
        task.save()

        sub1 = SubTask.objects.get(title="Gather information", task=task)
        sub1.deadline = date.today() - timedelta(days=2)
        sub1.save()

        sub2 = SubTask.objects.get(title="Create slides", task=task)
        sub2.description = "Create and format presentation slides"
        sub2.save()

        print("Обновления выполнены.")
    except Task.DoesNotExist:
        print("Задача не найдена.")


def delete_records():
    try:
        task = Task.objects.get(title="Prepare presentation")
        task.delete()
        print("Задача и связанные подзадачи удалены.")
    except Task.DoesNotExist:
        print("Задача уже удалена или не найдена.")


# Основной блок для запуска
if __name__ == "__main__":
    create_records()
    read_records()
    update_records()
    read_records()
    delete_records()
