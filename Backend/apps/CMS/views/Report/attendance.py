import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import now
from apps.ACCESS.models import User
from apps.BASE.views.base import AppAPIView
from apps.CMS.models import Check
import calendar
from django.contrib.auth import get_user_model


def AttendanceAPIView(request):
    today = now()
    year, month = today.year, today.month  # Current year and month
    first_day, last_day = 1, calendar.monthrange(year, month)[1]  # First and last day of the month

    # Fetch all users
    users = User.objects.all().order_by("id")  # Ensure correct model usage

    # Create column headers for the report
    columns = ["Name"] + [str(day) for day in range(1, last_day + 1)] + [" Present", "Absent"]

    # Initialize the report data
    report_data = []

    for user in users:
        # Fetch attendance records for the current month
        attendance = Check.objects.filter(user=user, created_at__year=year, created_at__month=month)

        # Create an attendance map for the month, defaulting to Absent (0)
        attendance_map = {day: 0 for day in range(1, last_day + 1)}

        # Update attendance_map: Mark Present days (1)
        for record in attendance:
            if record.checkin:  # Only consider days with check-in
                attendance_map[record.created_at.day] = 1

        # Calculate totals
        total_present = sum(attendance_map.values())
        total_absent = last_day - total_present

        # Append user data to report (Identity + Attendance for each day + Totals)
        report_data.append([user.identity] + list(attendance_map.values()) + [total_present, total_absent])

    # Convert report data to a DataFrame
    df = pd.DataFrame(report_data, columns=columns)

    # Generate Excel file response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="Monthly_User_Attendance_Report_{year}_{month}.xlsx"'
    df.to_excel(response, index=False)

    return response