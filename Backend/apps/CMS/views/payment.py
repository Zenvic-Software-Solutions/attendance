from datetime import date,datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.CMS.models import Loan,Payment
from apps.CMS.serializers import LoanNextDueSerializer,PaymentDueSerializer,CollectionSerializer
from apps.BASE.views import ListAPIViewSet

from datetime import datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend
from apps.BASE.pagination import AppPagination

class LoanNextDueListAPIView(ListAPIViewSet):
    serializer_class = LoanNextDueSerializer
    pagination_class = AppPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"customer__centre__id": ["exact"]}

    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(
            user=user, 
            balance_week__gt=0
        ).order_by("initiated_date")

    def list(self, request, *args, **kwargs):
        due_date_str = request.query_params.get("due_date")
        queryset = self.filter_queryset(self.get_queryset())

        if not due_date_str:
            return super().list(request, *args, **kwargs)

        try:
            target_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        serializer = self.get_serializer(queryset, many=True)
        loans = serializer.data

        filtered = []

        for loan in loans:
            matching_due_dates = []

            for d in loan["due_date"]:
                this_due_date = datetime.strptime(d["due_date"], "%Y-%m-%d").date()

                # Match selected due_date
                if this_due_date == target_date:
                    matching_due_dates.append(d)

            if matching_due_dates:
                filtered.append({
                    "id": loan["id"],
                    "uuid": loan["uuid"],
                    "loan_title": loan["loan_title"],
                    "customer": loan["customer"],
                    "centre": loan["centre"],
                    "initiated_date": loan["initiated_date"],
                    "interest_amount": loan["interest_amount"],
                    "balance_week": loan["balance_week"],
                    "due_date": matching_due_dates,
                })

        return Response({
            "data": {
                "count": len(filtered),
                "next": None,
                "previous": None,
                "results": filtered
            },
            "status": "success",
            "action_code": "DO_NOTHING"
        })



class PaymentListAPIView(ListAPIViewSet):
    serializer_class = PaymentDueSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        loan = Loan.objects.get(uuid=uuid)
        return Payment.objects.filter(loan=loan)
    




from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

class PaymentCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            loan_ids = request.data.get("loan_ids", [])
            paid_date = request.data.get("paid_date")
            user = request.user

            if not loan_ids:
                return Response({"error": "No loans selected"}, status=400)

            if not paid_date:
                return Response({"error": "paid_date is required"}, status=400)

            # convert date
            paid_date = date.fromisoformat(paid_date)

            response_data = []

            for loan_id in loan_ids:
                try:
                    loan = Loan.objects.get(id=loan_id, user=user)
                except Loan.DoesNotExist:
                    return Response({"error": f"Loan {loan_id} not found"}, status=404)

                # Create Payment
                payment = Payment.objects.create(
                    loan=loan,
                    amount=loan.interest_amount,    # OR amount from request?
                    status="Paid",
                    paid_date=paid_date,
                    user=user
                )
                
                if loan.balance > 0:
                    loan.balance = max(0, loan.balance - loan.interest_amount)

                # ↓ Decrease balance_week by 1
                if loan.balance_week > 0:
                    loan.balance_week -= 1
                if loan.balance_week > 0:
                    loan.initiated_date = loan.initiated_date + timedelta(days=7)
                loan.save()

                # ↓ Calculate next due date (from model function)
                next_due_date = loan.get_next_due_date()

                response_data.append({
                    "loan_id": loan.id,
                    "payment_id": payment.id,
                    "paid_date": paid_date,
                    "balance_week": loan.balance_week,
                    "next_due_date": next_due_date
                })

            return Response({"data":{
                "message": "Payments created successfully",
                "data": response_data
            } }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)



class CollectionAPIView(ListAPIViewSet):
    filterset_fields = {
        "loan__customer__centre__id":["exact"]
    }
    def get_queryset(self):
        today = date.today()
        user = self.request.user
        return Payment.objects.filter(user=user,paid_date=today)
    serializer_class = CollectionSerializer