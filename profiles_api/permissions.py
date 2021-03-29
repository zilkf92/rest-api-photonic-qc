from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allows Users to view only their respective Request Data"""

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser == True:
            return True

        return obj.id == request.user.id


class AdminViewList(permissions.BasePermission):
    """Allows Admin to see RequestData"""

    def has_permission(self, request, view):

        if view.action == "list":
            return request.user.is_superuser
        else:
            return True
