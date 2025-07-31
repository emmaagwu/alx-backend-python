from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, nothing to compare
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        editor = getattr(instance, "_edited_by", None) or instance.sender
        # Store previous content
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content,
            edited_by=editor,
        )
        instance.edited = True
