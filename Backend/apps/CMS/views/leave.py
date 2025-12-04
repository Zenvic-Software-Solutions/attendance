from apps.CMS.models import LeaveRequest
from apps.CMS.serializers import (
    LeaveRequestReadSerializer,
    LeaveRequestWriteSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.BASE.views import ListAPIViewSet,CUDAPIViewSet,AppAPIView


class LeaveRequestlistAPIView(ListAPIViewSet):
    filterset_fields ={
        "user":["exact"],
        "created_at":["gte","lte"],
        "leave_type":["exact"]
    }
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestReadSerializer


class LeaveRequestCUDAPIView(CUDAPIViewSet):
    permission_classes = [IsAuthenticated]
    queryset =LeaveRequest.objects.all()
    serializer_class = LeaveRequestWriteSerializer
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    

class LeaveStatusAPIView(AppAPIView):
    def patch(self, request, *args, **kwargs):
        uuid = request.data.get("uuid")
        status = request.data.get("status")

        if not uuid:
            return self.error_response("UUID is required.", status=400)

        if not status:
            return self.error_response("Status is required.", status=400)

        try:
            leave = LeaveRequest.objects.get(uuid=uuid)
        except LeaveRequest.DoesNotExist:
            return self.error_response("Leave request not found.", status=404)

        leave.status = status   # <-- FIXED FIELD NAME
        leave.save()

        return self.success_response(
            message="Leave status updated successfully.",
            data={"uuid": uuid, "status": status}
        )






