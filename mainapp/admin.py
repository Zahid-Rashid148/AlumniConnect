from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, AlumniProfile, MentorshipRequest, Message, Post, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'get_full_name', 'email', 'role', 'status', 'date_joined']
    list_filter = ['role', 'status', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_editable = ['status']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('AlumniConnect Info', {'fields': ('role', 'status', 'bio', 'phone', 'linkedin', 'avatar')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('AlumniConnect Info', {'fields': ('role', 'status', 'first_name', 'last_name', 'email')}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'branch', 'year', 'roll_number']
    search_fields = ['user__username', 'user__first_name', 'branch']
    list_filter = ['year', 'branch']


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'experience_years', 'graduation_year', 'is_open_to_mentor']
    search_fields = ['user__username', 'company', 'role', 'domain']
    list_filter = ['is_open_to_mentor', 'graduation_year']
    list_editable = ['is_open_to_mentor']


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'alumni', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['student__username', 'alumni__username']
    list_editable = ['status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_preview', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'content']

    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'post_type', 'company', 'created_at', 'is_active']
    list_filter = ['post_type', 'is_active', 'created_at']
    search_fields = ['title', 'company', 'author__username']
    list_editable = ['is_active']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notif_type', 'title', 'is_read', 'created_at']
    list_filter = ['notif_type', 'is_read']
    search_fields = ['user__username', 'title']
