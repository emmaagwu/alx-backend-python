# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Assumes the object has a `user` or `sender` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        return False
