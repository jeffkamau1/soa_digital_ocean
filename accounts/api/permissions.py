from rest_framework import permissions
from accounts.models import CustomUser


class IsTeamLead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_team_lead and request.user.is_authenticated
