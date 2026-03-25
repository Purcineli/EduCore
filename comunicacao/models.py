from django.conf import settings
from django.db import models

from core.models import BaseModel


class NoticeBoard(BaseModel):
    '''Notice board entry, optionally restricted by group.'''

    title = models.CharField(max_length=200, help_text='Notice title')
    content = models.TextField(help_text='Notice content/description')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notices',
        help_text='Author (usually a coordinator)',
    )
    target_groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='notices',
        help_text='Leave empty to show to all logged-in users. Select groups to restrict visibility.',
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'notice board'
        verbose_name_plural = 'notice boards'

    def __str__(self):
        status = 'Published' if self.is_published else 'Draft'
        return f'{self.title} ({status})'

    def publish(self):
        '''Mark this notice as published and set published_at timestamp.'''
        from django.utils import timezone
        if not self.is_published:
            self.is_published = True
            self.published_at = timezone.now()
            self.save(update_fields=['is_published', 'published_at', 'updated_at'])

    def is_visible_to(self, user):
        '''Return True if the notice should be visible to the given user.'''
        if not self.is_published:
            return False
        target = self.target_groups.all()
        if not target.exists():
            return True
        return user.groups.filter(pk__in=target).exists()


class Message(BaseModel):
    '''Direct message between two users.'''

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text='Message sender',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        help_text='Message receiver',
    )
    subject = models.CharField(max_length=200, help_text='Message subject')
    body = models.TextField(help_text='Message body')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return f'{self.sender.email} -> {self.receiver.email}: {self.subject}'

    def mark_as_read(self):
        '''Mark message as read and record the timestamp.'''
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at', 'updated_at'])
