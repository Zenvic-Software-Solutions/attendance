from apps.ACCESS.models import User
from apps.BASE.models import DEFAULT_BLANK_NULLABLE_FIELD_CONFIG, MAX_CHAR_FIELD_LENGTH, BaseModel
from django.db import models
from HELPERS.choices import LEAVE_STATUS
class Check(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    punch_in = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    punch_out = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    punch_date = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    latitude = models.FloatField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    longitude = models.FloatField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    leave_status = models.CharField(max_length=20,choices=LEAVE_STATUS,default="Absent")