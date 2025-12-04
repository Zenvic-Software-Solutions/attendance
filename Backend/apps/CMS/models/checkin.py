from apps.ACCESS.models import User
from apps.BASE.models import DEFAULT_BLANK_NULLABLE_FIELD_CONFIG, MAX_CHAR_FIELD_LENGTH, BaseModel
from django.db import models
from datetime import datetime,timedelta
from HELPERS.choices import LEAVE_STATUS
class Check(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    punch_in = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    punch_out = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    punch_date = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    latitude = models.FloatField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    longitude = models.FloatField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    leave_status = models.CharField(max_length=20,choices=LEAVE_STATUS,default="Absent")
    duration = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)

    def save(self, *args, **kwargs):

        # Calculate duration only if punch_in and punch_out exist
        if self.punch_in and self.punch_out:
            try:
                # Convert string → datetime.time
                time_in = datetime.strptime(self.punch_in, "%H:%M")
                time_out = datetime.strptime(self.punch_out, "%H:%M")

                # If punch_out is next day (optional)
                if time_out < time_in:
                    time_out += timedelta(days=1)

                # Calculate duration in hours
                diff = time_out - time_in
                hours = diff.total_seconds() / 3600

                self.duration = round(hours, 2)

            except Exception as e:
                # If error in time format, keep duration as 0
                self.duration = 0

        super().save(*args, **kwargs)