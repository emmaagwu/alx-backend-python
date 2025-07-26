# chats/views.py

from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedAndParticipant

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedAndParticipant]

    def get_queryset(self):
        # Only return conversations the user is part of
        return self.queryset.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedAndParticipant]

    def get_queryset(self):
        # Only messages in conversations the user participates in
        return self.queryset.filter(conversation__participants=self.request.user)
