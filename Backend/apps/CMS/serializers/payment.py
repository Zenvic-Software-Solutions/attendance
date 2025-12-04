from rest_framework import serializers
from apps.CMS.models import Loan,Payment
from datetime import timedelta, date
from apps.CMS.serializers import CentreReadSerializer



class LoanNextDueSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source="customer.identity", read_only=True)
    centre = serializers.CharField(source="customer.centre.identity", read_only=True)
    due_date = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "id",
            "uuid",
            "customer",
            "centre",
            "loan_title",
            "initiated_date",
            "interest_amount",
            "balance_week",
            "due_date",
        ]
    def get_due_date(self, obj):
        """
        Return only UNPAID due dates.
        Remove only due dates where a Payment exists with matching paid_date.
        """

        if not obj.initiated_date or obj.balance_week == 0:
            return []

        start = obj.initiated_date.date()
        first_due = start + timedelta(days=1)

        # Generate due dates only for remaining balance weeks
        full_due_dates = [
            first_due + timedelta(days=7 * (week - 1))
            for week in range(1, obj.balance_week + 1)
        ]

        unpaid_list = []
        from apps.CMS.models import Payment

        for week_no, due_date in enumerate(full_due_dates, start=1):

            # ❌ Remove ONLY paid due dates
            is_paid = Payment.objects.filter(
                loan=obj,
                paid_date=due_date,
                status="Paid"
            ).exists()

            # ✔ Keep only UNPAID dates
            if not is_paid:
                unpaid_list.append({
                    "week_no": week_no,
                    "due_date": due_date.strftime("%Y-%m-%d"),
                    "interest_amount": str(obj.interest_amount)
                })

        return unpaid_list

 
class PaymentDueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = [
            "id",
            "uuid",
            "amount",
            "status",
            "paid_date"
        ]



class CollectionSerializer(serializers.ModelSerializer):
    loan = serializers.CharField(source="loan.loan_title",read_only=True)
    customer_name = serializers.CharField(source="loan.customer.identity",read_only=True)
    customer_phone = serializers.CharField(source="loan.customer.phone_number",read_only=True)
    centre = serializers.CharField(source="loan.customer.centre.identity",read_only=True)
    # centre = CentreReadSerializer()
    class Meta:
        model = Payment
        fields = [
            "id",
            "uuid",
            "loan",
            "customer_name",
            "customer_phone",
            "centre",
            "amount",
            "status"
        ]