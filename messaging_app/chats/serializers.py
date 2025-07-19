from rest_framework import serializers
from .models import User, Message, Conversation

# =========================
# User Serializer
# =========================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'created_at']


# =========================
# Message Serializer
# =========================

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # nested sender info

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']


# =========================
# Conversation Serializer
# =========================

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)  # related_name='messages'

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
