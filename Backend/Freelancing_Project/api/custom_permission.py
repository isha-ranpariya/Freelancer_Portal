from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    """
    Custom permission to allow only freelancers to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a freelancer
        if request.user.is_authenticated and request.user.is_freelancer:
            return False
        return True
