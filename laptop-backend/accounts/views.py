from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, ProfileSerializer
from .permissions import IsAdmin, IsEmployee, IsCustomer


# 1. Đăng ký tài khoản
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# 2. Đăng nhập
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Vui lòng nhập tên đăng nhập và mật khẩu"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Tên đăng nhập hoặc mật khẩu không đúng"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            "message": "Đăng nhập thành công",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)


# 3. Kiểm tra quyền Admin
class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "message": "Bạn có quyền Admin"
        })


# 4. Kiểm tra quyền Employee
class EmployeeOnlyView(APIView):
    permission_classes = [IsEmployee]

    def get(self, request):
        return Response({
            "message": "Bạn có quyền Employee hoặc Admin"
        })


# 5. Kiểm tra quyền Customer
class CustomerOnlyView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        return Response({
            "message": "Bạn có quyền Customer"
        })


# 6. Xem và cập nhật thông tin cá nhân
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_role(self, user):
        if user.is_superuser:
            return "Admin"
        elif user.groups.filter(name="Employee").exists():
            return "Employee"
        elif user.groups.filter(name="Customer").exists():
            return "Customer"
        return "Unassigned"

    # Xem thông tin cá nhân
    def get(self, request):
        serializer = ProfileSerializer(request.user)

        return Response({
            **serializer.data,
            "role": self.get_role(request.user)
        })

    # Cập nhật thông tin cá nhân
    def patch(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Cập nhật thông tin thành công",
            "user": {
                **serializer.data,
                "role": self.get_role(request.user)
            }
        })

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response(
                {"error": "Vui lòng nhập đầy đủ mật khẩu"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Mật khẩu cũ không đúng"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user=user)
        except ValidationError as error:
            return Response(
                {"error": error.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({
            "message": "Đổi mật khẩu thành công"
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Vui lòng cung cấp Refresh Token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Đăng xuất thành công"},
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {"error": "Refresh Token không hợp lệ hoặc đã bị thu hồi"},
                status=status.HTTP_400_BAD_REQUEST
            )
