import uuid
from contextlib import suppress
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from apps.BASE.managers import BaseObjectManagerQuerySet


MAX_CHAR_FIELD_LENGTH = 512
DEFAULT_NULLABLE_FIELD_CONFIG = {
    "default": None,
    "null": True,
}
DEFAULT_BLANK_NULLABLE_FIELD_CONFIG = {
    **DEFAULT_NULLABLE_FIELD_CONFIG,
    "blank": True,
}


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # created_by = models.ForeignKey(
    #     to=settings.AUTH_USER_MODEL,
    #     related_name="created_%(class)s",
    #     on_delete=models.SET_DEFAULT,
    #     **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,
    # )

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseObjectManagerQuerySet.as_manager()

    class Meta:
        abstract = True

    @classmethod
    def get_model_fields(cls):
        return cls._meta.fields

    @classmethod
    def get_all_model_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_model_field_names(cls, exclude=[]):
        exclude = ["id", "created_by", "created", *exclude]
        return [_.name for _ in cls.get_model_fields() if _.name not in exclude]

    @classmethod
    def get_model_field(cls, field_name, fallback=None):
        with suppress(FieldDoesNotExist):
            return cls._meta.get_field(field_name)
        
        return fallback


class FileOnlyModel(BaseModel):
    class Meta(BaseModel.Meta):
        abstract = True


class BaseIdentityModel(BaseModel):
    class Meta(BaseModel.Meta):
        abstract = True

    identity = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, verbose_name="Name/Title"
    )

    description = models.TextField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)

    def __str__(self):
        return self.identity


class UUIDForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['to_field'] = 'uuid'
        
        kwargs.setdefault('on_delete', models.CASCADE)
        kwargs.setdefault('blank', True) 
        kwargs.setdefault('null', True) 
        
        super().__init__(*args, **kwargs)
