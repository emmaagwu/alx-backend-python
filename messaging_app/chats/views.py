from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth.models import User

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'updated_at']  # Optional fields for ordering

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation__id=conversation_id)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = Conversation.objects.get(pk=conversation_id)
        message = serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

