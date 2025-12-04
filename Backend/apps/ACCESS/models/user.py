from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.BASE.managers import UserManager
from apps.BASE.models import (
    BaseModel,
    MAX_CHAR_FIELD_LENGTH,
    DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,
)
from apps.BASE.model_fields import SingleChoiceField

from HELPERS.choices import GENDER,DOMAIN



# Custom User Model
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    employee_id = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    
    identity = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    email = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,unique= True)
    phone_number = models.CharField(max_length=10,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    confirm_password = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    dob = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    address = models.TextField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    city = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    gender = models.CharField(max_length=50,choices=GENDER,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    domain = models.CharField(max_length=50,choices=DOMAIN,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    mode = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.email}"
