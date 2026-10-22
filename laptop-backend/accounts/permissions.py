
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Chỉ quản trị viên mới có quyền truy cập."

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsEmployee(BasePermission):
    message = "Chỉ nhân viên hoặc quản trị viên được truy cập."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user.is_authenticated
            and (
                user.is_superuser
                or user.groups.filter(name="Employee").exists()
            )
        )


class IsCustomer(BasePermission):
    message = "Chỉ khách hàng mới có quyền truy cập."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user.is_authenticated
            and user.groups.filter(name="Customer").exists()
        )
