from rest_framework import serializers

class DailyReportSerializer(serializers.Serializer):
    today_paid_total = serializers.DecimalField(max_digits=15, decimal_places=2)
    today_unpaid_count = serializers.IntegerField()
    today_paid_count = serializers.IntegerField()
    loan_due_today = serializers.IntegerField()


class CenterReportSerializer(serializers.Serializer):
    center = serializers.CharField()
    total_customers = serializers.IntegerField()
    total_loans = serializers.IntegerField()
    today_paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    today_unpaid = serializers.DecimalField(max_digits=15, decimal_places=2)


class CustomerReportSerializer(serializers.Serializer):
    customer = serializers.CharField()
    total_loans = serializers.IntegerField()
    total_paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_unpaid = serializers.DecimalField(max_digits=15, decimal_places=2)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)


class LoanReportSerializer(serializers.Serializer):
    loan_title = serializers.CharField()
    customer = serializers.CharField()
    principal_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    interest_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    status = serializers.CharField()
