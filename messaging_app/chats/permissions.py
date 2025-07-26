from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Conversation, Message


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
    

class IsAuthenticatedAndParticipant(permissions.BasePermission):
    """
    Custom permission:
    - Only allow access to authenticated users
    - Only allow access to participants of a conversation
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission.
        obj can be a Message or Conversation.
        """
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        elif isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False
