from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):
    """
    Custom permission to only allow access to librarians.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a librarian
        return request.user.is_authenticated and request.user.is_librarian
