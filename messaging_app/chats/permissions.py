from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Conversation, Message

class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        return False


class IsAuthenticatedAndParticipant(BasePermission):
    """
    Allows access only to authenticated users who are participants in the conversation.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        elif isinstance(obj, Message):
            # Handle GET, PUT, PATCH, DELETE
            if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
                return request.user in obj.conversation.participants.all()
            
            # POST is handled differently (usually in create, see views.py)
            return False

        return False
