from rest_framework import permissions
from accounts.models import CustomUser


class IsIncidentManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == "Incident Manager" and request.user.is_authenticated
