from django.contrib import admin
from django.utils import timezone

from .models import Message, NoticeBoard


@admin.register(NoticeBoard)
class NoticeBoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'published_at', 'created_at')
    list_filter = ('is_published', 'created_at', 'target_groups')
    search_fields = ('title', 'content')
    filter_horizontal = ('target_groups',)
    readonly_fields = ('created_at', 'updated_at', 'published_at', 'historical')

    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'author'),
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at', 'target_groups'),
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at', 'historical'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        '''Auto-set published_at when is_published becomes True for the first time.'''
        if obj.is_published and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'receiver__email', 'subject', 'body')
    readonly_fields = ('created_at', 'updated_at', 'read_at', 'historical')

    fieldsets = (
        ('Message', {
            'fields': ('sender', 'receiver', 'subject', 'body'),
        }),
        ('Status', {
            'fields': ('is_read', 'read_at'),
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at', 'historical'),
            'classes': ('collapse',),
        }),
    )
