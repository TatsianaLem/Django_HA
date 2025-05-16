from rest_framework import serializers
from task_manager.models import (
    Task,
    SubTask,
    Category
)
from datetime import date
from django.utils import timezone

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)

        if name != instance.name and Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": "Категория с таким названием уже существует."})
        # instance.name = name
        # instance.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']

class SubTaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']


class TaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        if value < date.today():
        #if value < timezone.now():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
        return value

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
            'created_at',
            'subtasks'
        ]
        # fields = "__all__"
        # exclude = ['updated_at']

