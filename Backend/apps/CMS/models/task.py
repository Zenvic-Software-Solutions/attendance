from django.db import models
from apps.BASE.models import BaseModel,MAX_CHAR_FIELD_LENGTH,DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
from apps.ACCESS.models import User
from HELPERS.choices import STATUS

class Category(BaseModel):
    identity = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)




class Task(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    task_name = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    hours = models.TimeField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    status = models.CharField(max_length=20,choices=STATUS,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    description = models.TextField()