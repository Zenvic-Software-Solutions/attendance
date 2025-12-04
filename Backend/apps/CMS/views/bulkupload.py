import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.db import transaction,IntegrityError
from datetime import datetime
from apps.CMS.models import Centre,Customer, Loan
class LoanBulkUploadAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def clean_phone(self, value):
        if pd.isna(value) or str(value).strip() == "":
            return None
        return str(value).strip()

    @transaction.atomic
    def post(self, request):
        user = request.user
        excel_file = request.FILES.get("file")

        if not excel_file:
            return Response({"error": "Excel file is required"}, status=400)

        try:
            df = pd.read_excel(excel_file)
        except:
            return Response({"error": "Invalid Excel file"}, status=400)

        required_cols = [
            "customer_identity", "customer_phone",
            "centre_identity",
            "nominee_identity", "nominee_phone",
            "loan_title", "principal_amount",
            "interest_amount", "initiated_date",
            "loan_date", "total_week","balance_week","balance"
        ]

        for col in required_cols:
            if col not in df.columns:
                return Response({"error": f"Missing column: {col}"}, status=400)

        loan_count = 0
        errors = []

        for index, row in df.iterrows():

            customer_phone = self.clean_phone(row["customer_phone"])
            nominee_phone = self.clean_phone(row["nominee_phone"])

            # ✅ Customer phone is mandatory
            if not customer_phone:
                errors.append(f"Row {index + 1}: Customer phone number is missing")
                continue

            # ✅ Centre
            centre, _ = Centre.objects.get_or_create(
                user=user,
                identity=row["centre_identity"]
            )

            # ✅ Customer (Reuses existing if same phone)
            try:
                customer, _ = Customer.objects.get_or_create(
                    user=user,
                    phone_number=customer_phone,
                    defaults={
                        "identity": row["customer_identity"],
                        "centre": centre
                    }
                )
            except IntegrityError:
                # Phone already exists → fetch existing customer
                customer = Customer.objects.get(
                    user=user,
                    phone_number=customer_phone
                )

            # ✅ Nominee (Optional phone, optional record)
            nominee = None
            if nominee_phone:
                try:
                    nominee, _ = Customer.objects.get_or_create(
                        user=user,
                        phone_number=nominee_phone,
                        defaults={
                            "identity": row["nominee_identity"],
                            "centre": centre
                        }
                    )
                except IntegrityError:
                    nominee = Customer.objects.get(
                        user=user,
                        phone_number=nominee_phone
                    )

            # ✅ Convert dates
            initiated_date = pd.to_datetime(row["initiated_date"]) if row["initiated_date"] else None
            loan_date = pd.to_datetime(row["loan_date"]) if row["loan_date"] else None

            # ✅ Create Loan
            Loan.objects.create(
                user=user,
                customer=customer,
                nominee=nominee,
                loan_title=row["loan_title"],
                principal_amount=row["principal_amount"],
                interest_amount=row["interest_amount"],
                initiated_date=initiated_date,
                loan_date=loan_date,
                total_week=row["total_week"],
                balance_week=row["balance_week"],
                balance=row["balance"]
            )

            loan_count += 1

        return Response({
            "message": "Bulk loan upload completed",
            "created": loan_count,
            "errors": errors
        }, status=201)



import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from io import BytesIO

class LoanBulkDownloadSampleAPIView(APIView):
    def get(self, request):
        # Define the column headings
        columns = [
            "customer_identity",
            "customer_phone",
            "centre_identity",
            "nominee_identity",
            "nominee_phone",
            "loan_title",
            "principal_amount",
            "interest_amount",
            "initiated_date",
            "loan_date",
            "total_week",
            "balance",
            "balance_week",
        ]

        # Create an empty DataFrame with only headings
        df = pd.DataFrame(columns=columns)

        # Save to in-memory Excel
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        # Return as downloadable file
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="loan_bulk_sample.xlsx"'
        return response
