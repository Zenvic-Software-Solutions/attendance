from rest_framework import serializers
from apps.ACCESS.models import User
from apps.CMS.models import Category,Task
from apps.BASE.serializers import ReadOnlySerializer,WriteOnlySerializer,read_serializer

class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","uuid","identity"]



class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["identity"]


class TaskReadSerializer(ReadOnlySerializer):
    category_details = read_serializer(Category,meta_fields=["id",
                                                             "uuid","identity"])(source="category")
    user_details = read_serializer(User,meta_fields=["id","uuid","employee_id","identity"])(source="user")
    class Meta(ReadOnlySerializer.Meta):
        model = Task
        fields = [
            "id",
            "uuid",
            "task_name",
            "user_details",
            "category_details",
            "created_at",
            "status"
        ]

class TaskWriteSerializer(WriteOnlySerializer):
    class Meta(WriteOnlySerializer.Meta):
        model = Task
        fields = [
            "task_name",
            "created_at",
            "status",
            "description",
            "hours"
        ]


