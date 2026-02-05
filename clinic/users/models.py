# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


# -----------------------------------------------------
# ROLE MODEL
# -----------------------------------------------------
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name


# -----------------------------------------------------
# PERMISSION MODEL
# -----------------------------------------------------
class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.name


# -----------------------------------------------------
# ROLE_PERMISSION MODEL (Role ↔ Permission Mapping)
# -----------------------------------------------------
class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"

    def __str__(self):
        return f"{self.role.name} → {self.permission.name}"


# -----------------------------------------------------
# CUSTOM USER MODEL
# -----------------------------------------------------
class User(AbstractUser):
    # FK instead of text role
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    # Disable default username behaviour
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is still required by Django

    def __str__(self):
        return f"{self.email} ({self.role})"


# -----------------------------------------------------
# ACTIVITY LOG MODEL
# -----------------------------------------------------
class ActivityLog(models.Model):
    ACTIONS = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=50, choices=ACTIONS)
    table_name = models.CharField(max_length=100)
    record_id = models.IntegerField(null=True, blank=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.user} - {self.action_type} ({self.table_name})"
