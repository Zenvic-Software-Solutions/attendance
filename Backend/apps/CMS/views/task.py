from apps.ACCESS.models import User
from apps.CMS.models import Category,Task
from apps.CMS.serializers import (
    CategoryReadSerializer,
    CategoryWriteSerializer,
    TaskListReadSerializer,TaskWriteSerializer
)
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from apps.BASE.views import ListAPIViewSet,CUDAPIViewSet
from rest_framework.response import Response



class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return CategoryReadSerializer
        return CategoryWriteSerializer

class TaskCMSAPIView(ListAPIViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListReadSerializer



class TaskCUDAPIView(CUDAPIViewSet):
    permission_classes = [IsAuthenticated]
    queryset =Task.objects.all()
    serializer_class = TaskWriteSerializer
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


