from .checkin import CheckInOutAPI,UserPunchHistory,PunchListAPIView
from .check_list import CheckListAPIView,PresentListAPIView,AbsentListAPIView,UserAttendanceListAPIView
from .dashboard import (
    DashboardAPIView,
    DailyAbsentAPIView,
    DailyPresentAPIView,
    MonthlyAbsentAPIView,
    MonthlyPresentAPIView
)

from .task import CategoryAPIView,TaskListAPIView,TaskCUDAPIView
from .leave import LeaveRequestlistAPIView,LeaveRequestCUDAPIView,LeaveStatusAPIView



from .userpunch import (
    CategoryListAPIView,
    CategoryCreateAPIView,
    UserLeaveDetailAPIView,
    UserLeaveListAPIView,
    UserPunchListAPIView,
    UserTaskListAPIView,
    UserTaskRetrieveAPIView
)


from .attendence import (
    AttendencealllistAPIView,
    UserMetaAPIView,
)
