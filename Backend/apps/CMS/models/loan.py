from apps.BASE.models import BaseModel,MAX_CHAR_FIELD_LENGTH,DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
from apps.ACCESS.models import User
from apps.CMS.models import Customer,Centre
from django.db import models

from datetime import timedelta, date
class LoanBill(BaseModel):
    file = models.ImageField(upload_to="files/bill/image")

class Loan(BaseModel):
    loan_id = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    loan_title = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    user = models.ForeignKey(User,on_delete=models.CASCADE,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,related_name="customer")
    nominee = models.ForeignKey(Customer,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    principal_amount = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    interest_amount = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    balance = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    initiated_date = models.DateTimeField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    loan_date = models.DateTimeField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    # due_date = models.DateTimeField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    total_week =models.PositiveIntegerField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    balance_week =models.PositiveIntegerField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    bill_image = models.ManyToManyField(LoanBill,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)


    def save(self, *args, **kwargs):
        if not self.loan_id:

            user = self.user
            centre = self.customer.centre if self.customer else None

            # Filter loan by user + centre
            last_loan = Loan.objects.filter(
                user=user,
                customer__centre=centre
            ).order_by("id").last()

            # Generate next number
            if last_loan and last_loan.loan_id:
                # loan format: LOAN-U1-C2-000001  → split last part
                last_number = int(last_loan.loan_id.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            # Create unique loan id
            self.loan_id = f"LOAN-{new_number:04d}"

        super().save(*args, **kwargs)


    def get_next_due_date(self):
        """
        next due date = initiated_date + (weeks_paid * 7 days)
        do NOT return next due date when loan is completed
        """
        # Loan fully finished
        if self.balance_week == 0:
            return None

        weeks_paid = self.total_week - self.balance_week
        return self.initiated_date.date() + timedelta(days=weeks_paid * 7)
    