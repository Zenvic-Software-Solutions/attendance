from django.urls import path
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.ACCESS.serializers.user import RegisterSerializer, UserListReadOnlySerializer,UserListDetailOnlySerializer,UserWriteOnlySerializer, UserDetailSerializer,UserDetailEditSerializer
from apps.BASE.permissions import NonAuthenticatedAPIMixin
from apps.BASE.views import AppAPIView, ListAPIViewSet, CUDAPIViewSet, AbstractLookUpFieldMixin,AppCreateAPIView
from django.contrib.auth import authenticate
from apps.ACCESS.models import User
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as django_logout
from apps.BASE.pagination import BaseViewMixin


# Register View
class RegisterView(AppCreateAPIView,NonAuthenticatedAPIMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

   

class LoginView(AppAPIView, NonAuthenticatedAPIMixin):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        # 1. Invalid email or password
        if not user:
            return self.send_error_response({"error": "Invalid email or password"})

        # 2. Staff users cannot login
        if user.is_staff is True:
            return self.send_error_response({"error": "Staff users are not allowed to login"})

        # 3. Only active users can login
        if user.is_active is False:
            return self.send_error_response({"error": "Your account is deactivated"})

        # 4. Successful login
        token, _ = Token.objects.get_or_create(user=user)

        data = {
            "email": user.email,
            "token": token.key,
            "uuid": user.uuid
        }

        return self.send_response(data=data)

class AdminLoginView(AppAPIView, NonAuthenticatedAPIMixin):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        # Invalid credentials
        if user is None:
            return self.send_error_response(
                {"message": "Invalid email or password."}
            )

        # User exists but not staff
        if not user.is_staff:
            return self.send_error_response(
                {"error": "Access denied. Admin users only."}
            )

        # Valid staff user
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            "email": user.email,
            "token": token.key,
            "uuid": user.uuid,
        }
        return self.send_response(data=data)



# Logout View 
class LogoutView(AppAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user= self.get_authenticated_user()
        if user:
            Token.objects.filter(user=user).delete()
        django_logout(request)
        return self.send_response(data={"Successfully logged out"})
            
       

# class GetAuthUserDetails(AppAPIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         # Helper method to safely extract role attributes
#         def get_role_attr(attr, default=False):
#             return getattr(user.role, attr, default) if hasattr(user, "role") and user.role else default

#         return self.send_response(
#             data={
#                 "id": user.id,
#                 "identity": user.identity if hasattr(user, "identity") else None,
#                 "email": user.email if hasattr(user, "email") else None,
                
#                 "inventory_access": get_role_attr("inventory_access"),
#                 "stock_access": get_role_attr("stock_access"),
#                 "invoice_access": get_role_attr("invoice_access"),
#                 "employee_access": get_role_attr("employee_access"),
#                 "report_access": get_role_attr("report_access"),
#                 "log_access": get_role_attr("log_access"),
#             }
#         )



class UserDetailAPIView(AppAPIView):
    def get(self, request, *args, **kwargs):
        user = self.get_authenticated_user()
        
        if not user:
            return self.send_error_response({"detail": "Invalid User"})
        data = {
            "id": user.id,
            "uuid": user.uuid,
            "identity": user.identity,
            "email": user.email,
            "phone_number": user.phone_number,
            "dob":user.dob,
            "address":user.address,
            "city":user.city,
            "gender":user.gender,
            "domain":user.domain,
            "is_active":user.is_active,
            "mode":user.mode,
        }
        return self.send_response(data)
    
class UserDetailEditAPIView(AppAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.get_authenticated_user()
        serializer = UserDetailEditSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return self.send_response(data=serializer.data)

        return self.send_error_response(serializer.errors)

class UserListAppAPIView(BaseViewMixin,ListAPIViewSet):
    search_fields = ["phone_number","email","identity","gender","domain"]
    queryset = User.objects.all()
    serializer_class= UserListReadOnlySerializer

    all_table_columns = {
        "identity":"Name",
        "phone_number":"Phone Number",
        "is_active" :"Active",
        "node":"Mode"
    }

    def get_meta_for_table(self):
        data = {
            "columns":self.all_table_columns,
            "filters":self.all_filters,
            "filter_data":{
                
            }
        }
        return data
    
from django.shortcuts import get_object_or_404
class UserRetrieveAppAPIView(AppAPIView):
    def get(self, request, uuid,*args, **kwargs):
        
        if not uuid:
            return self.send_error_response({"detail": "Invalid UUID"})
        user = get_object_or_404(User, uuid=uuid)
        data = {
            "id": user.id,
            "uuid": user.uuid,
            "identity": user.identity,
            "email": user.email,
            "phone_number": user.phone_number,
            "dob":user.dob,
            "address":user.address,
            "city":user.city,
            "gender":user.gender,
            "domain":user.domain,
            
        }
        return self.send_response(data)

    
class UserCUDAppAPIView(CUDAPIViewSet):
    queryset = User.objects.all()
    serializer_class= UserWriteOnlySerializer
    

class UserDetailsAPIView(AbstractLookUpFieldMixin, AppAPIView, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class= UserDetailSerializer