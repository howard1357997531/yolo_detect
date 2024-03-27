from django.contrib import admin
from .models import (Profile, Alert, AlertPrivate, CameraSplitSetting, CameraSplitSettingPrivate,
                     AlertPureQuantity, AlertPureQuantityPrivate)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'image')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_checked', 'alert_image_code', 'alert_image_quantity', 'alert_video_code', 'alert_video_quantity', 'alert_folder_code', 'alert_folder_quantity', 'created_at', 'modified_at')

@admin.register(AlertPrivate)
class AlertPrivateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_quantity', 'is_checked', 'alert_image_code', 'alert_image_quantity', 'alert_video_code', 'alert_video_quantity', 'alert_folder_code', 'alert_folder_quantity', 'created_at', 'modified_at')

@admin.register(CameraSplitSetting)
class CameraSplitSettingAdmin(admin.ModelAdmin):
    list_display = ('camera_name', 'x_start', 'x_end', 'y_start', 'y_end', 'modified_at')

@admin.register(CameraSplitSettingPrivate)
class CameraSplitSettingPrivateAdmin(admin.ModelAdmin):
    list_display = ('user', 'camera_name', 'x_start', 'x_end', 'y_start', 'y_end', 'modified_at')

@admin.register(AlertPureQuantity)
class AlertPureQuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_checked', 'name', 'code', 'created_at', 'modified_at')

@admin.register(AlertPureQuantityPrivate)
class AlertPureQuantityPrivateAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_checked', 'user', 'name', 'code', 'created_at', 'modified_at')

