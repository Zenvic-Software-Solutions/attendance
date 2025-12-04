from django.apps import apps
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class BulkFileUploadSerializer(serializers.Serializer):
    
    file = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )
    
    def __init__(self, *args, **kwargs):
        model_name = kwargs.pop("model_name", None)
        app_label = kwargs.pop("app_label", "CMS")

        if not model_name:
            raise ValueError("Model name is required.")

        try:
            self.model = apps.get_model(app_label, model_name)
        except LookupError:
            raise ValueError(f"Model '{model_name}' not found in the app '{app_label}'.")

        self.file_field = kwargs.pop("file_field", "file")
        if not hasattr(self.model, self.file_field):
            raise ValueError(f"Model '{model_name}' does not have a field named '{self.file_field}'.")
        
        super().__init__(*args, **kwargs)

    def validate_file(self, files):
        for file in files:
            if file.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(f"File '{file.name}' exceeds the size limit of 5MB.")
        return files

    def create(self, validated_data):
        files = validated_data.get("file")
        file_field = self.file_field

        instances = [self.model(**{file_field: file}) for file in files]
        return self.model.objects.bulk_create(instances)


class BulkFileUploadView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        model_name = request.data.get('model')
        app_label = request.data.get('app_label', 'CMS')
        

        if not model_name:
            return Response({'error': 'Model name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BulkFileUploadSerializer(
            data=request.data, model_name=model_name, app_label=app_label
        )
        
        if serializer.is_valid():
            created_files = serializer.save()
            return Response(
                {
                    "message": "Files uploaded successfully.",
                    "file_ids": [getattr(instance, 'id', None) for instance in created_files],
                    "file_uuids": [getattr(instance, 'uuid', None) for instance in created_files if hasattr(instance, 'uuid')],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
