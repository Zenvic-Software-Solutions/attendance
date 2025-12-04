from django.db import models
from apps.BASE.models import BaseModel,MAX_CHAR_FIELD_LENGTH,DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
from apps.CMS.models import Loan
from apps.ACCESS.models import User 

from datetime import timedelta, date
class Payment(BaseModel):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Closed', 'Closed'),
    ]

    loan = models.ForeignKey(
        'Loan',
        on_delete=models.SET_NULL,
        **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Unpaid'
    )
    paid_date = models.DateField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)


