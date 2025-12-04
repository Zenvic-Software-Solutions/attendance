
from apps.CMS.serializers import UserPunchListSerializer,UserIdentitySerializer
from rest_framework.generics import ListAPIView
from apps.CMS.models import Check
from apps.ACCESS.models import User
from apps.BASE.pagination import BaseViewMixin
from rest_framework.response import Response

class UserMetaAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserIdentitySerializer
    



class AttendencealllistAPIView(BaseViewMixin, ListAPIView):
    """
    API to list attendance data for all users with
    filtering by punch_date (gte, lte) and user__identity.
    """
    serializer_class = UserPunchListSerializer
    queryset = Check.objects.all()
    filterset_fields = {
        "punch_date": ["gte", "lte"],
        "user__identity": ["exact"],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        
        # No pagination fallback
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "data": {
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            }
        })