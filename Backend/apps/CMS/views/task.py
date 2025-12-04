from apps.ACCESS.models import User
from apps.CMS.models import Category,Task
from apps.CMS.serializers import (
    CategoryReadSerializer,
    CategoryWriteSerializer,TaskDetailSerializer,
    TaskReadSerializer,TaskWriteSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from datetime import datetime

from rest_framework.response import Response



class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return CategoryReadSerializer
        return CategoryWriteSerializer



class TaskAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        today = datetime.now().date()  
        user = self.request.user
        return Task.objects.filter(
            is_active=True,
            user=user,
            created_at__date=today 
        )

    def get_serializer_class(self):
        if self.action == "list":
            return TaskReadSerializer
        if self.action == "retrieve":
            return TaskDetailSerializer
        return TaskWriteSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "data": {
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            }
        })
