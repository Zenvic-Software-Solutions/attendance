from apps.BASE.views import ListAPIViewSet
from apps.CMS.models import Check
from apps.CMS.serializers import CheckInReadSerializer
from apps.ACCESS.models import User
from django.utils.timezone import now


class CheckListAPIView(ListAPIViewSet):
    search_fields=["user__identity"]
    
    filterset_fields={
        "checkin":["exact"],
        "checkout":["exact"],
        "created_at":["gte","lte"]
    }
    queryset = Check.objects.all()
    serializer_class = CheckInReadSerializer
    all_table_columns={
        "user_details.identity":"Name",
        "checkin" :"Chenck In",
        "checkout":"Check Out",
        "created_at":"Date"
    }
    all_filters ={
        "created_at":"Date",
    
    }

    def get_meta_for_table(self):
        data ={
            "columns":self.all_table_columns,
            "filters":self.all_filters,
            "filter_data":{
                "user":self.serialize_for_filter(User.objects.all())
            }
        }
        return data
        



class PresentListAPIView(ListAPIViewSet):
    
    serializer_class = CheckInReadSerializer

    def get_queryset(self):
        today = now().date()
        return Check.objects.filter(checkin__isnull=False,created_at=today)
    
    
    

class AbsentListAPIView(ListAPIViewSet):
    serializer_class = CheckInReadSerializer

    def get_queryset(self):
        today = now().date()
        return Check.objects.filter(checkin__isnull=True,created_at=today)
    

class UserAttendanceListAPIView(ListAPIViewSet):
    filterset_fields={
        "checkin":["exact"],
        "checkout":["exact"],
        "created_at":["gte","lte"]
    }
    serializer_class=CheckInReadSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        user = User.objects.get(uuid = uuid)
        return Check.objects.filter(user =user)
    all_table_columns={
        "checkin" :"Chenck In",
        "checkout":"Check Out",
        "created_at":"Date"
    }
    all_filters ={
        "created_at":"Date",
    
    }

    def get_meta_for_table(self,*args,**kwargs):
        data ={
            "columns":self.all_table_columns,
            "filters":self.all_filters,
            "filter_data":{
            }
        }
        return self.send_response(data)
