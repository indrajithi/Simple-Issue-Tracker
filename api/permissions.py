from rest_framework.permissions import BasePermission
from .models import Issue

class IsOwner(BasePermission):
    """Custom permission class to allow only Issue owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the Issue owner."""
        if isinstance(obj, Issue):
            return obj.created_by == request.user
        return obj.created_by == request.user