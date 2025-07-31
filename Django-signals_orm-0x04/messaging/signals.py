from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
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

@receiver(post_delete, sender=User)
def cleanup_user_related(sender, instance, **kwargs):
    """
    Defensive cleanup: most of the related data should cascade automatically
    if the models use on_delete=CASCADE. This ensures nothing is left orphaned,
    and handles fields like edited_by (which uses SET_NULL) gracefully.
    """
    # Delete messages where they were sender or receiver (redundant if CASCADE already)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications directly tied to the user
    Notification.objects.filter(user=instance).delete()

    # For histories where they were the editor, null out (since edited_by uses SET_NULL)
    MessageHistory.objects.filter(edited_by=instance).update(edited_by=None)