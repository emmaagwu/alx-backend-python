from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'updated_at']
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(
            conversation__id=conversation_id,
            conversation__user=self.request.user
        )

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(pk=conversation_id, user=self.request.user)
        serializer.save(sender=self.request.user, conversation=conversation)


