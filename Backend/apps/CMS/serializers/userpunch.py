from rest_framework import serializers
from apps.ACCESS.models import User
from apps.CMS.models import Check,Task,LeaveRequest,Category

class UserIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uuid",
            "identity"
        ]

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","uuid","identity"]
class CategoryCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["identity"]

class UserPunchListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.identity",read_only=True)
    class Meta:
        model = Check
        fields =[
            "id",
            "uuid",
            "user",
            "punch_in",
            "punch_out",
            "punch_date",
            "leave_status"
        ]



class UserTaskListSerializer(serializers.ModelSerializer):
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
        
        ]
class UserTaskDetailSerializer(serializers.ModelSerializer):
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
            "description"
        
        ]
class LeaveSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.identity",read_only=True)
    class Meta:
        model = LeaveRequest
        fields =["id","uuid","user","leave_type","from_date","to_date","duration"]
class LeaveDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.identity",read_only=True)
    class Meta:
        model = LeaveRequest
        fields =["id","uuid","user","leave_type","from_date","to_date","duration","reason"]