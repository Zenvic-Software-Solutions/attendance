from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    # GetAuthUserDetails,
    UserDetailAPIView,
    UserListAppAPIView,
    UserDetailEditAPIView,
    UserDetailsAPIView,
    UserCUDAppAPIView,
    AdminLoginView,
    UserRetrieveAppAPIView,
)
from rest_framework.routers import SimpleRouter

app_name = "access"

router = SimpleRouter()

# User management routes
router.register("user/list", UserListAppAPIView, basename="user-list")
router.register("user/cud", UserCUDAppAPIView, basename="user-cud")



urlpatterns = [
    # Authentication routes
    path("login/", LoginView.as_view(), name="login"),
    path("admin/login/", AdminLoginView.as_view(), name="admin-login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # User-specific routes
    # path("user/details/", GetAuthUserDetails.as_view(), name="user_details"),
    path("user/detail/", UserDetailAPIView.as_view(), name="user_update"),
    path("user/retrieve/<uuid>/", UserRetrieveAppAPIView.as_view(), name="user_detail_retrieve"),
    path("user/update/", UserDetailEditAPIView.as_view(), name="user_detail_edit"),
    
    # Router URLs
    path("", include(router.urls)),
]
