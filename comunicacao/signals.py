from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Message, NoticeBoard


@receiver(pre_save, sender=NoticeBoard)
def notice_board_pre_save(sender, instance, **kwargs):
    '''
    Log a publication event into historical when a NoticeBoard transitions
    from draft to published for the first time.
    '''
    if not instance.pk:
        # New instance — nothing to compare yet; log on post_save instead.
        return

    try:
        old = NoticeBoard.objects.get(pk=instance.pk)
    except NoticeBoard.DoesNotExist:
        return

    if not old.is_published and instance.is_published:
        event = {
            'event': 'published',
            'by': instance.author.email,
            'timestamp': timezone.now().isoformat(),
        }
        key = f'event_{timezone.now().isoformat()}'
        if instance.historical is None:
            instance.historical = {}
        instance.historical[key] = event


@receiver(post_save, sender=NoticeBoard)
def notice_board_post_save(sender, instance, created, **kwargs):
    '''Log a creation event into historical when a NoticeBoard is first created.'''
    if created:
        event = {
            'event': 'created',
            'by': instance.author.email,
            'timestamp': timezone.now().isoformat(),
        }
        key = f'event_{timezone.now().isoformat()}'
        if instance.historical is None:
            instance.historical = {}
        instance.historical[key] = event
        # Use update to avoid re-triggering signals.
        NoticeBoard.objects.filter(pk=instance.pk).update(historical=instance.historical)


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    '''Log a creation event into historical when a Message is first created.'''
    if created:
        event = {
            'event': 'created',
            'from': instance.sender.email,
            'to': instance.receiver.email,
            'timestamp': timezone.now().isoformat(),
        }
        key = f'event_{timezone.now().isoformat()}'
        if instance.historical is None:
            instance.historical = {}
        instance.historical[key] = event
        Message.objects.filter(pk=instance.pk).update(historical=instance.historical)
