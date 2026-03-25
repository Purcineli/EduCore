from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Guardian, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Audit', {'fields': ('created_at', 'updated_at', 'historical')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'historical', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'relationship_type', 'created_at')
    list_filter = ('relationship_type',)
    search_fields = ('parent__email', 'student__email')
    readonly_fields = ('created_at', 'updated_at', 'historical')
