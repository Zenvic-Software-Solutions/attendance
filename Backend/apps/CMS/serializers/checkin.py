from apps.ACCESS.models import User
from apps.BASE.serializers import ReadOnlySerializer, read_serializer
from apps.CMS.models import Check
from rest_framework import serializers

class CheckInReadSerializer(ReadOnlySerializer):
    user_details = read_serializer(User,meta_fields=["id","uuid","identity"])(source="user")
    is_absent = serializers.SerializerMethodField()
    class Meta(ReadOnlySerializer.Meta):
        model = Check
        fields = [
            "id",
            "uuid",
            "checkin",
            "checkout",
            "created_at",
            "user_details",
            "duration",
            "is_absent"
        ]
    def get_is_absent(self,obj):
        return obj.checkin is None
    
class PunchReadSerializer(ReadOnlySerializer):
    user_details = read_serializer(User,meta_fields=["id","uuid","employee_id","identity"])(source="user")

    class Meta(ReadOnlySerializer.Meta):
        model = Check
        fields = [
            "id",
            "uuid",
            "punch_in",
            "punch_out",
            "punch_date",
            "duration",
            "user_details"
        ]