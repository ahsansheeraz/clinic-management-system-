# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Role, Permission, RolePermission, ActivityLog
)


# ----------------------------
# USER ADMIN
# ----------------------------
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff',
                                           'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'role', 'first_name', 'last_name',
                       'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)


# ----------------------------
# ACTIVITY LOG ADMIN
# ----------------------------
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'table_name', 'record_id', 'created_at')
    list_filter = ('action_type', 'table_name', 'user')
    search_fields = ('table_name', 'user__email')
