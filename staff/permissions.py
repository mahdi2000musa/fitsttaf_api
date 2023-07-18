from rest_framework.permissions import BasePermission, SAFE_METHODS
from staff.models import *


class IsPresenterOrAdminUserOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        profile = Profile.objects.get(user=request.user)
        return obj.profile == profile

