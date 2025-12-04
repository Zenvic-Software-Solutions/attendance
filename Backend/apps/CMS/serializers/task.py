from rest_framework import serializers
from apps.ACCESS.models import User
from apps.CMS.models import Category,Task
from apps.BASE.serializers import ReadOnlySerializer,WriteOnlySerializer,read_serializer

class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","uuid","identity"]



class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["identity"]


