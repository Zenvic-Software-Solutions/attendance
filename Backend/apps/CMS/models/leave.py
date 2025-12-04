from apps.ACCESS.models import User
from HELPERS.choices import LEAVE_TYPE
from apps.BASE.models import BaseModel,MAX_CHAR_FIELD_LENGTH,DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
from django.db import models




class LeaveRequest(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    leave_type = models.CharField(max_length=20,choices=LEAVE_TYPE,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    from_date = models.DateField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    to_date = models.DateField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    reason = models.TextField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    duration = models.PositiveBigIntegerField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)