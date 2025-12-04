from apps.ACCESS.models import User
from apps.CMS.models import Category,Task
from apps.CMS.serializers import (
    CategoryReadSerializer,
    CategoryWriteSerializer,
    TaskReadSerializer,
    TaskWriteSerializer
)
from apps.BASE.pagination import AppPagination
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from apps.BASE.views import ListAPIViewSet,CUDAPIViewSet
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return CategoryReadSerializer
        return CategoryWriteSerializer

class TaskListAPIView(ListAPIView):
    pagination_class = AppPagination
    queryset =Task.objects.all()
    serializer_class = TaskReadSerializer
    

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response({
            "data": {
                "count": response.data.get("count"),
                "next": response.data.get("next"),
                "previous": response.data.get("previous"),
                "results": response.data.get("results"),
            },
            "status": "success",
            "action_code": "DO_NOTHING"
        })


class TaskCUDAPIView(CUDAPIViewSet):
    permission_classes = [IsAuthenticated]
    queryset =Task.objects.all()
    serializer_class = TaskWriteSerializer
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


