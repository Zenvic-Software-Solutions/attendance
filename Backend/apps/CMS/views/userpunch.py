from apps.CMS.models import Category,Task,LeaveRequest,Check
from apps.ACCESS.models import User
from apps.CMS.serializers import (
    CategoryCUDSerializer,
    CategoryListSerializer,
    UserPunchListSerializer,
    UserTaskDetailSerializer,
    UserTaskListSerializer,
    LeaveDetailSerializer,
    LeaveSerializer,
    
)
from rest_framework import viewsets,generics,filters  

from rest_framework.response import Response
from apps.BASE.pagination import BaseViewMixin

class CategoryCreateAPIView(BaseViewMixin,viewsets.ModelViewSet):
    
    
    queryset = Category.objects.all()
    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        return CategoryCUDSerializer
    
class CategoryListAPIView(BaseViewMixin, generics.ListAPIView):
    queryset = Category.objects.all()
    search_fields = ["identity"] 
    def get_serializer_class(self):
        # 'self.action' doesn't exist in generics.ListAPIView — it's a viewset attribute.
        # So, you can directly return the list serializer here.
        return CategoryListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # Replace 'results' key with 'list'
            paginated_data = paginated_response.data
            paginated_data["results"] = paginated_data.pop("results", [])
            return Response({"data": paginated_data})
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "data": serializer.data
        })



class UserPunchListAPIView(BaseViewMixin, generics.ListAPIView):
    """
    API to list punch details of a specific user (filtered by UUID).
    Supports filtering by punch_date (gte, lte) and user__identity.
    Example: /api/user/<uuid>/punch-list/
    """
    serializer_class = UserPunchListSerializer
    filterset_fields = {
        "punch_date": ["exact"],
        "user__identity": ["exact"]
    }

    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        user = User.objects.get(uuid=uuid)
        queryset = Check.objects.filter(user=user, is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # Replace 'results' key with 'list'
            paginated_data = paginated_response.data
            paginated_data["results"] = paginated_data.pop("results", [])
            return Response({"data": paginated_data})
       
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "data": {
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            }
        })


class UserTaskListAPIView(BaseViewMixin, generics.ListAPIView):
    """
    API to list all tasks of a specific user based on UUID.
    Example URL: /api/user/<uuid>/tasks/
    """

    serializer_class = UserTaskListSerializer
    filterset_fields = {
        "user__identity": ["exact"],
        "category__identity":["exact"]
    }

    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        user = User.objects.get(uuid=uuid)
        queryset = Task.objects.filter(user=user, is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # Replace 'results' key with 'list'
            paginated_data = paginated_response.data
            paginated_data["results"] = paginated_data.pop("results", [])
            return Response({"data": paginated_data})
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "data": {
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            }
        })

class UserTaskRetrieveAPIView(BaseViewMixin, generics.RetrieveAPIView):
    lookup_field = "uuid"
    queryset = Task.objects.all()
    serializer_class = UserTaskDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # fetch single object
        serializer = self.get_serializer(instance)

        return Response({
            "data": serializer.data  # no count/next/previous for single object
        })


class UserLeaveListAPIView(BaseViewMixin, generics.ListAPIView):
    """
    API to list all leave requests for a specific user.
    Example: /api/user/<uuid>/leaves/
    """
    serializer_class = LeaveSerializer
    filterset_fields = {
        "user__identity": ["exact"]
    }

    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        user = User.objects.get(uuid=uuid)
        queryset = LeaveRequest.objects.filter(user=user, is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # Replace 'results' key with 'list'
            paginated_data = paginated_response.data
            paginated_data["results"] = paginated_data.pop("results", [])
            return Response({"data": paginated_data})
        
        # Fallback if pagination not used
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "data": {
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            }
        })

class UserLeaveDetailAPIView(BaseViewMixin, generics.RetrieveAPIView):
    lookup_field = "uuid"
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # fetch single object
        serializer = self.get_serializer(instance)

        return Response({
            "data": serializer.data  # no count/next/previous for single object
        })
