from apps.BASE.views import AppAPIView
from apps.CMS.models import Loan,Payment,Customer
from apps.ACCESS.models import User
from datetime import datetime,date,timedelta
from django.db.models import Sum

class Dashboard(AppAPIView):
    def get(self, request, *args, **kwargs):
        today = date.today()
        user = request.user

        if not user:
            return self.send_error_response({"error": "User not found"})

        # 🔹 GET centre filter
        centre_id = request.query_params.get("centre_id")
        due_date = request.query_params.get("initiated_date")

        # SIMPLE TOTALS (SAFE WITH OR 0)
        purchased_customer_ids = Loan.objects.filter(
            user=user
        ).values_list("customer_id", flat=True)

        customer_count = Customer.objects.filter(
            user=user,
            id__in=purchased_customer_ids
        ).count()

        balance = Loan.objects.filter(user=user).aggregate(
            total=Sum("balance")
        )["total"] or 0

        # ACTIVE LOANS ONLY
        loans = Loan.objects.filter(user=user, balance_week__gt=0)

        today_interest = 0
        today_balance = 0

        for loan in loans:

            if not loan.initiated_date:
                continue  # avoid error if null

            # FIRST DUE = initiated_date + 1 Day
            first_due = loan.initiated_date.date() + timedelta(days=1)

            # ALL UPCOMING DUE DATES
            due_dates = [
                first_due + timedelta(days=7 * (week_no - 1))
                for week_no in range(1, (loan.balance_week or 0) + 1)
            ]

            # CHECK IF TODAY IS A DUE DATE
            if today in due_dates:

                paid_today = Payment.objects.filter(
                    loan=loan,
                    paid_date=today,
                    status="Paid"
                ).exists()

                # TODAY INTEREST (UNPAID ONLY)
                if not paid_today:
                    today_interest += loan.interest_amount or 0

                # TODAY BALANCE (UNPAID ONLY)
                if not paid_today:
                    today_balance += loan.interest_amount or 0
                else:
                    today_balance += 0

        loan_count = Loan.objects.filter(user=user).count()

        # TODAY AMOUNT PAID — FIXED (None → 0)
        today_amount = Payment.objects.filter(
            user=user,
            paid_date=today
        ).aggregate(total=Sum("amount"))["total"] or 0

        # FIX
        today_interest = today_balance + today_amount

        # ✅ DEFAULT: GLOBAL TODAY BALANCE
        today_centre_balance_total = today_balance

        # ---------------------------------------------------------
        #       ONLY MINIMAL CHANGE STARTS HERE
        # ---------------------------------------------------------
        if centre_id:
            # reset only when centre filter applied
            today_centre_balance_total = 0

            centre_loans = Loan.objects.filter(
                user=user,
                customer__centre__id=centre_id,
                initiated_date=due_date,
                balance_week__gt=0
            )

            for loan in centre_loans:

                if not loan.initiated_date:
                    continue

                first_due = loan.initiated_date.date() + timedelta(days=1)

                due_dates = [
                    first_due + timedelta(days=7 * (week_no - 1))
                    for week_no in range(1, (loan.balance_week or 0) + 1)
                ]

                if today in due_dates:

                    paid_today = Payment.objects.filter(
                        loan=loan,
                        paid_date=today,
                        status="Paid"
                    ).exists()

                    if not paid_today:
                        today_centre_balance_total += loan.interest_amount or 0
        # ---------------------------------------------------------
        #       ONLY MINIMAL CHANGE ENDS HERE
        # ---------------------------------------------------------

        # FINAL RESPONSE DATA
        data = {
            "customer_count": customer_count,
            "balance": balance,
            "today_balance": today_balance,
            "today_amount": today_amount,
            "today_interest": today_interest,
            "loan_count": loan_count,

            # 👉 FILTERED OR DEFAULT TODAY BALANCE
            "today_centre_balance_total": today_centre_balance_total,
        }

        return self.send_response(data=data)
