from apps.CMS.models import LeaveRequest
from apps.ACCESS.models import User
from rest_framework import serializers 
from apps.BASE.serializers import ReadOnlySerializer,WriteOnlySerializer,read_serializer



class LeaveRequestReadSerializer(ReadOnlySerializer):
    user_details = read_serializer(User,meta_fields=["id","uuid","employee_id","identity"])(source="user")
    class Meta(ReadOnlySerializer.Meta):
        model = LeaveRequest
        fields=[
            "id",
            "uuid",
            "user_details",
            "leave_type",
            "from_date",
            "to_date",
            "duration",
            "created_at",
            "leave_request",
        ]


class LeaveRequestWriteSerializer(WriteOnlySerializer):
    class Meta:
        model = LeaveRequest
        fields=[
            "leave_type",
            "from_date",
            "to_date",
            "reason",
            "duration",
            "leave_request",
        ]