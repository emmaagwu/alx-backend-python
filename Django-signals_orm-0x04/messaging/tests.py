from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello!'
        )

        # Check that a Notification was created for the receiver
        notification = Notification.objects.filter(user=self.receiver, message=message).first()
        self.assertIsNotNone(notification)

class MessageEditHistoryTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="pass")
        self.receiver = User.objects.create_user(username="bob", password="pass")

    def test_edit_logs_history_with_editor(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Original")
        # simulate edit by sender
        msg.content = "Edited content"
        msg._edited_by = self.sender
        msg.save()

        history = MessageHistory.objects.filter(message=msg).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, "Original")
        self.assertEqual(history.edited_by, self.sender)
        self.assertTrue(msg.edited)
