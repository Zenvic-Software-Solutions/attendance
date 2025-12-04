from apps.CMS.models import LeaveRequest
from apps.ACCESS.models import User
from rest_framework import serializers 



class LeaveRequestReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.identity",read_only=True)
    class Meta:
        model = LeaveRequest
        fields=[
            "id",
            "uuid",
            "user",
            "leave_type",
            "from_date",
            "to_date",
            "duration"
        ]

class LeaveRequestDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.identity",read_only=True)
    class Meta:
        model = LeaveRequest
        fields=[
            "id",
            "uuid",
            "user",
            "leave_type",
            "from_date",
            "to_date",
            "duration",
            "reason",
        ]
class LeaveRequestWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields=[
            "leave_type",
            "from_date",
            "to_date",
            "reason",
            "duration"
        ]