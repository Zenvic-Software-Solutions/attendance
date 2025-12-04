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
            "is_absent"
        ]
    def get_is_absent(self,obj):
        return obj.checkin is None