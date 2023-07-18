from rest_framework.permissions import BasePermission, SAFE_METHODS

from staff.models import Profile
from tasks.models import Task


class IsTeamLeader(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.role == 'T'


class IsAssigner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        p = Profile.objects.get(user=request.user)
        return obj.assigner == p


class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        p = Profile.objects.get(user=request.user)
        return obj.participant == p


class IsParticipantORAssigner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        profile = Profile.objects.get(user=request.user)
        return obj.participant == profile or obj.assigner == profile


class IsOwnerORAdminORReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True

        owner = Profile.objects.get(user=request.user)
        return obj.profile == owner
