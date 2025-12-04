from apps.CMS.models import LeaveRequest
from apps.CMS.serializers import (
    LeaveRequestDetailSerializer,
    LeaveRequestReadSerializer,
    LeaveRequestWriteSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class LeaveRequestAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field= "uuid"
    def get_queryset(self):
        user = self.request.user
        return LeaveRequest.objects.filter(user=user)
    def get_serializer_class(self):
        if self.action == "list":
            return LeaveRequestReadSerializer
        if self.action == "retrieve":
            return LeaveRequestDetailSerializer
        return LeaveRequestWriteSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


