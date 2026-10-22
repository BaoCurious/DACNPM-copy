
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    LoginView,
    AdminOnlyView,
    EmployeeOnlyView,
    CustomerOnlyView,
    ProfileView,
    ChangePasswordView,
    LogoutView,
)

urlpatterns = [
    # Đăng ký và đăng nhập
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # JWT Authentication
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Phân quyền
    path("admin-only/", AdminOnlyView.as_view(), name="admin_only"),
    path("employee-only/", EmployeeOnlyView.as_view(), name="employee_only"),
    path("customer-only/", CustomerOnlyView.as_view(), name="customer_only"),

    # Thông tin cá nhân
    path("profile/", ProfileView.as_view(), name="profile"),

    # Đổi mật khẩu
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),

    # Đăng xuất
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
