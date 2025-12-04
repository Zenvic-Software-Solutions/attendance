from apps.ACCESS.models import User
from apps.BASE.views import AppAPIView,ListAPIViewSet
from apps.CMS.models import Check
from django.utils.timezone import now
from apps.CMS.models import Check
from apps.CMS.serializers import UserPunchListSerializer


class DashboardAPIView(AppAPIView):
    def get(self, request):
        current_date = now().date()
        current_month = now().month
        current_year = now().year

        # Total employees
        employee_count = User.objects.count()

        # Today's present employees
        present_count = Check.objects.filter(created_at__date=current_date).count()

        # This month's present employees
        month_present_count = Check.objects.filter(
            created_at__year=current_year,
            created_at__month=current_month
        ).count()

        # Calculate absentees
        absent_count = employee_count - present_count
        month_absent_count =  month_present_count - employee_count 

        data = {
            "employee_count": employee_count,
            "present_count": present_count,
            "absent_count": absent_count,
            "month_present_count": month_present_count,
            "month_absent_count": month_absent_count
        }

        return self.send_response(data)
    


class DailyPresentAPIView(ListAPIViewSet):
    current_date = now().date()
    def get_queryset(self):
        current_date = now().date()
        return Check.objects.filter(
            punch_date=current_date,
            leave_status="Present"
        )
    serializer_class = UserPunchListSerializer
    
    

class DailyAbsentAPIView(ListAPIViewSet):
    serializer_class = UserPunchListSerializer

    def get_queryset(self):
        current_date = str(now().date())

        # Get all users who have a Check record for today
        checked_in_users = Check.objects.exclude(
            punch_date=current_date  # use punch_date, not created_at
        ).values_list('user_id', flat=True)

        # Exclude them — get users who did NOT check in today
        return User.objects.exclude(id__in=checked_in_users)

class MonthlyPresentAPIView(ListAPIViewSet):
    current_month = now().month
    current_year = now().year
    queryset = Check.objects.filter(leave_status="Present",created_at__year=current_year,created_at__month=current_month)
    serializer_class = UserPunchListSerializer
    
    
class MonthlyAbsentAPIView(ListAPIViewSet):
    current_month = now().month
    current_year = now().year
    queryset = Check.objects.filter(leave_status="Absent",created_at__year=current_year,created_at__month=current_month)
    serializer_class = UserPunchListSerializer
    
    



