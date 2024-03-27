from django.contrib import admin
from .models import (Video, VideoPrivate, VideoOutput, VideoOutputPrivate,
                     AlertVideo, AlertVideoNormalUser, AlertVideoSuperUser)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'videofile')

@admin.register(VideoPrivate)
class VideoPrivateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'videofile')

@admin.register(VideoOutput)
class VideoOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'file_url', 'created_at', 'modified_at')

@admin.register(VideoOutputPrivate)
class VideoOutputPrivateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'file_url', 'created_at', 'modified_at')

@admin.register(AlertVideo)
class AlertVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'code', 'is_checked', 'created_at', 'modified_at')

@admin.register(AlertVideoNormalUser)
class AlertVideoNormalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'source', 'code', 'is_checked', 'created_at', 'modified_at')

@admin.register(AlertVideoSuperUser)
class AlertVideoSuperUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'source', 'code', 'is_checked', 'created_at', 'modified_at')