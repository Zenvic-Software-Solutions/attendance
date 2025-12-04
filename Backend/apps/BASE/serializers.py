from datetime import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.db import models
from apps.BASE.config import CUSTOM_ERRORS_MESSAGES

# Mixin to customize error messages for serializer fields
class CustomErrorMessagesMixin:
    def get_display(self, field_name):
        """Formats field names for error messages by replacing underscores with spaces."""
        return field_name.replace("_", " ")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update error messages for each field in the serializer
        for field_name, field in getattr(self, "fields", {}).items():
            field_type = field.__class__.__name__
            if field_type == "ManyRelatedField":
                field.error_messages.update(CUSTOM_ERRORS_MESSAGES["ManyRelatedField"])
                field.child_relation.error_messages.update(
                    CUSTOM_ERRORS_MESSAGES["PrimaryKeyRelatedField"]
                )
            elif field_type == "PrimaryKeyRelatedField":
                field.error_messages.update(CUSTOM_ERRORS_MESSAGES["PrimaryKeyRelatedField"])
            else:
                field.error_messages.update({
                    "blank": f"Please enter your {self.get_display(field_name)}",
                    "null": f"Please enter your {self.get_display(field_name)}",
                })

# Base serializer with additional utility methods
class AppSerializer(CustomErrorMessagesMixin, Serializer):
    def get_request(self):
        """Retrieve the request object from the serializer context."""
        return self.context.get("request")

    def get_user(self):
        """Retrieve the user object from the request, if authenticated."""
        request = self.get_request()
        return request.user if request else None

# Model serializer with extended functionality
class AppModelSerializer(AppSerializer, ModelSerializer):
    class Meta:
        pass

# Serializer for handling write-only operations
class WriteOnlySerializer(AppModelSerializer):
    class Meta:
        model = None
        fields = []
        extra_kwargs = {}

    def __init__(self, *args, **kwargs):
        meta = getattr(self, "Meta", None)
        if meta:
            extra_kwargs = getattr(meta, "extra_kwargs", {})
            for field in meta.fields:
                extra_kwargs.setdefault(field, {"required": True})
            meta.extra_kwargs = extra_kwargs
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        """Automatically set the `created_by` field to the authenticated user during creation."""
        instance = super().create(validated_data)
        if hasattr(instance, "created_by") and not instance.created_by:
            user = self.get_user()
            instance.created_by = user if user and user.is_authenticated else None
            instance.save()
        return instance

    def get_validated_data(self, key=None):
        """Retrieve validated data for a specific key or the entire data."""
        return self.validated_data if not key else self.validated_data.get(key)

    def to_internal_value(self, data):
        """Normalize empty values to None, except for falsy values like False, 0, or empty lists."""
        data = super().to_internal_value(data)
        return {k: (None if not v and v not in [False, 0, []] else v) for k, v in data.items()}

    def to_representation(self, instance):
        """Override representation to include meta information."""
        return self.get_meta_initial()

    def get_meta_urls(self):
        """Generate a list of URLs for related file fields in the instance."""
        if not self.instance:
            return []

        urls = []
        for field_name in self.fields:
            model_field = self.Meta.model.get_model_field(field_name)
            if model_field and model_field.related_model:
                related_instance = getattr(self.instance, field_name, None)
                if isinstance(related_instance, (models.Manager, models.QuerySet)):
                    urls.extend({"id": item.id, field_name: item.file.url} for item in related_instance.all() if hasattr(item, "file") and item.file)
                elif related_instance and hasattr(related_instance, "file"):
                    urls.append({"id": related_instance.id, field_name: related_instance.file.url})
        return urls

    def get_meta_initial(self):
        """Retrieve initial values for fields in the instance."""
        if not self.instance:
            return {}
        initial_data = {}
        for field in self.Meta.fields:
            value = getattr(self.instance, field, None)
            if hasattr(value, "all"):
                initial_data[field] = list(value.values_list("id", flat=True))
            elif hasattr(value, "id"):
                initial_data[field] = value.id
            else:
                initial_data[field] = value
        return initial_data

    def get_meta_for_create(self):
        """Meta information for object creation."""
        return {"meta": self.get_meta(), "initial": {}}

    def get_meta_for_update(self):
        """Meta information for object update."""
        return {"meta": self.get_meta(), "initial": self.get_meta_initial(), "urls": self.get_meta_urls()}

    def get_meta(self):
        """Retrieve general meta information."""
        return {}

# Serializer for read-only operations
class ReadOnlySerializer(AppModelSerializer):
    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

# Factory function to create a read-only serializer dynamically
def read_serializer(meta_model, meta_fields=None, init_fields_config=None, first_only=False):
    meta_fields = meta_fields or ["id", "uuid", "identity"]

    class _ListSerializer(serializers.ListSerializer):
        def to_representation(self, instance):
            if first_only:
                instance = instance.all()[:1] if hasattr(instance, "all") else [instance]
            return super().to_representation(instance)

    class _Serializer(ReadOnlySerializer):
        class Meta(ReadOnlySerializer.Meta):
            model = meta_model
            fields = meta_fields
            list_serializer_class = _ListSerializer

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if init_fields_config:
                for field, value in init_fields_config.items():
                    self.fields[field] = value

    return _Serializer

# Simplified serialization of querysets
def simple_serialize_queryset(fields, queryset):
    return [{**item, "id": str(item["id"])} for item in queryset.only(*fields).values(*fields)] if "id" in fields else queryset.only(*fields).values(*fields)

# Simplified serialization of a single instance
def simple_serialize_instance(instance, keys, parent_data=None, display=None):
    parent_data = parent_data or {}
    display = display or {}

    for key in keys:
        value = getattr(instance, key.split(".")[0], None)
        for sub_key in key.split(".")[1:]:
            value = getattr(value, sub_key, None) if value else None
        parent_data[display.get(key, key)] = value if isinstance(value, (int, float)) else str(value) if value else value

    return parent_data

# Custom field for serializing file models to URLs
class FileModelToURLField(serializers.Field):
    def to_internal_value(self, data):
        raise NotImplementedError

    def to_representation(self, value):
        return value.file.url if value and hasattr(value, "file") else None
