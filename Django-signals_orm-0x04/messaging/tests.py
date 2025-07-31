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

class UserDeletionCleanupTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username="usera", password="pass")
        self.user_b = User.objects.create_user(username="userb", password="pass")

        # user_a sends a message to user_b
        self.msg = Message.objects.create(sender=self.user_a, receiver=self.user_b, content="Original")
        # edit it so history exists
        self.msg.content = "Edited"
        self.msg._edited_by = self.user_a
        self.msg.save()

        # create a notification for user_b manually to simulate
        Notification.objects.create(user=self.user_b, message=self.msg)

    def test_deleting_user_cleans_up_related_data(self):
        # delete user_a (sender and editor)
        self.user_a.delete()

        # message sent by user_a should be gone (cascade)
        self.assertFalse(Message.objects.filter(pk=self.msg.pk).exists())

        # history should still exist if tied to message? (message was deleted so its histories are gone)
        self.assertFalse(MessageHistory.objects.filter(message__pk=self.msg.pk).exists())

        # deleting user_b should also remove their notifications
        self.user_b.delete()
        self.assertFalse(Notification.objects.filter(user=self.user_b).exists())
