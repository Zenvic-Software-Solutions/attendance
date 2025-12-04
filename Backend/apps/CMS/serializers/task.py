from rest_framework import serializers
from apps.ACCESS.models import User
from apps.CMS.models import Category,Task



class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","uuid","identity"]



class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["identity"]



class TaskDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.identity",read_only=True)
    category = serializers.CharField(source="category.identity",read_only=True)
    class Meta:
        model = Task
        fields = [
            "id",
            "uuid",
            "user",
            "category",
            "task_name",
            "hours",
            "status",
            "description",
            "created_at",
        ]
class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "category",
            "task_name",
            "hours",
            "status",
            "description"
        ]
class TaskReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.identity",read_only=True)
    category = serializers.CharField(source="category.identity",read_only=True)
    class Meta:
        model = Task
        fields = [
            "id",
            "uuid",
            "user",
            "category",
            "task_name",
            "hours",
            "status",
            "created_at"
        ]

