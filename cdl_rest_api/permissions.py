from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    # Has_object_permission gets called every time a request is made
    # to the API that we assign our permission to
    # has_object_permission function defines permission class
    def has_object_permission(self, request, obj):
        """Check if user is trying to edit their own profile"""
        # Allow users to view other users profiles but only able
        # to make changes to their own profile
        # Checks if the request is in the safe methods,
        # if it is, request is allowed to go through
        if request.method in permissions.SAFE_METHODS:
            return True
        # If it is not in the safe methods, the result of
        # the boolean expression is returned
        return obj.id == request.user.id


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow Users to view only their own request objects
    but allow superuser alias admin to view all objects.
    """

    # has_object_permission refers to object permission
    def has_object_permission(self, request, obj):

        if request.user.is_superuser == True:
            return True

        return obj.id == request.user.id


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins alias is_staff are allowed to post or
    put (change) data. All other methods are allowed for the
    all users.
    """

    # has_permission refers to user permission
    def has_permission(self, request, view):

        if request.method == "POST" or request.method == "PUT":
            return request.user.is_staff
        else:
            return True


class UpdateOwnStatus(permissions.BasePermission):
    """
    Allow only object owners to create and change objects and
    allow all other users to read data.
    (IsOwnerOrReadOnly)
    """

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
