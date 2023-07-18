from django.contrib import admin
from .models import *


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('subject',  'description', 'file', 'status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at', )
    search_fields = ('subject', 'description')
    fieldsets = (
        ('Task-info', {
            'fields': ('subject', 'description', 'status', 'file')
        }),
        ('Task-time', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Task-users', {
            'fields': ('participant', 'assigner')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'profile', 'file', 'task', 'created_at', 'updated_at')

