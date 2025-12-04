from rest_framework.routers import SimpleRouter
from django.urls import path

#Bulk-Upload-Files
from HELPERS import BulkFileUploadView, ActiveStatusChange, ArchieveStatusChange
from apps.CMS.views import (
    CheckInOutAPI,
    CheckListAPIView,
    PresentListAPIView,
    AbsentListAPIView,
    UserAttendanceListAPIView,
    DashboardAPIView,
    UserPunchHistory,
    CategoryAPIView,TaskCMSAPIView,TaskCUDAPIView,
    LeaveRequestlistAPIView,
    LeaveRequestCUDAPIView,
    CategoryListAPIView,
    UserTaskRetrieveAPIView,
    UserLeaveDetailAPIView,
    UserLeaveListAPIView,
    UserPunchListAPIView,
    UserTaskListAPIView,
    AttendencealllistAPIView,
    UserMetaAPIView,
    CategoryCreateAPIView,
    DailyAbsentAPIView,
    DailyPresentAPIView,
    MonthlyAbsentAPIView,
    MonthlyPresentAPIView,
    LeaveStatusAPIView,
    PunchListAPIView,
    
    
)
from apps.CMS.views.Report import AttendanceAPIView

app_name = "cms"
API_URL_PREFIX = "api/"

router = SimpleRouter()

router.register("check/list",CheckListAPIView,basename="check-list")
router.register("category",CategoryCreateAPIView,basename="category")
# router.register("category/list",CategoryListAPIView,basename="category-list")
router.register("user/meta",UserMetaAPIView,basename="meta")
router.register("task",TaskCUDAPIView,basename="task")
router.register("task/list",TaskCMSAPIView,basename="task-list")
router.register("leave/request",LeaveRequestCUDAPIView,basename="leave-request")
router.register("leave/list",LeaveRequestlistAPIView,basename="leave-list")
router.register("daily/absent",DailyAbsentAPIView,basename="daily/absent")
router.register("daily/present",DailyPresentAPIView,basename="daily/present")
router.register("monthly/absent",MonthlyAbsentAPIView,basename="monthly/absent")
router.register("monthly/present",MonthlyPresentAPIView,basename="monthly/present")
router.register("attendence/list",PunchListAPIView,basename="punch-list")
urlpatterns = [
    path("check/",CheckInOutAPI.as_view()),
    path("check/present/", PresentListAPIView.as_view({'get': 'list'}), name="present-users"),
    path("check/absent/", AbsentListAPIView.as_view({'get': 'list'}), name="absent-users"),
    path("check/attendance/<uuid>/", UserAttendanceListAPIView.as_view({'get': 'list'}), name="attendance-users"),
    path("check/attendance/<uuid>/table-meta/", UserAttendanceListAPIView.as_view({'get': 'get_meta_for_table'}), name="attendance-users"),
    path("dashboard/", DashboardAPIView.as_view()),
    path("attendance/report/", AttendanceAPIView),
    path("punch-history/", UserPunchHistory.as_view(), name="user-punch-history"),
    path("user/punch/list/<uuid>/",UserPunchListAPIView.as_view()),
    path("user/task/list/<uuid>/",UserTaskListAPIView.as_view()),
    path("user/task/retrieve/<uuid>/",UserTaskRetrieveAPIView.as_view()),
    path("user/leave/<uuid>/",UserLeaveListAPIView.as_view()),
    path("user/leave/retrieve/<uuid>/",UserLeaveDetailAPIView.as_view()),
    path("category/list/",CategoryListAPIView.as_view()),
    path("leave/status/",LeaveStatusAPIView.as_view()),
  
   
] + router.urls