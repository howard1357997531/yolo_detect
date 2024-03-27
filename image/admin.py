from django.contrib import admin
from .models import (Image, ImagePrivate, ImageMultipleFolder, ImageMultipleFolderPrivate, 
                     AlertImage, AlertImageNormalUser, AlertImageSuperUser,
                     AlertImageMultipleFolder, AlertImageMultipleFolderPrivate)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'image_file', 'created_at', 'modified_at')
    #　ordering = ('id',)

@admin.register(ImagePrivate)
class ImagePrivateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'image_file', 'created_at', 'modified_at')

@admin.register(ImageMultipleFolder)
class ImageMultipleFolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'name', 'image_file', 'created_at', 'modified_at')

@admin.register(ImageMultipleFolderPrivate)
class ImageMultipleFolderPrivateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'name', 'image_file', 'created_at', 'modified_at')

@admin.register(AlertImage)
class AlertImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'code', 'is_checked', 'created_at', 'modified_at')

@admin.register(AlertImageNormalUser)
class AlertImageNormalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'source', 'code', 'is_checked', 'created_at', 'modified_at')

@admin.register(AlertImageSuperUser)
class AlertImageSuperUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'source', 'code', 'is_checked', 'created_at', 'modified_at')

@admin.register(AlertImageMultipleFolder)
class AlertImageMultipleFolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'folder_code', 'is_checked', 'is_deleted', 'image_quantity', 'created_at', 'modified_at')

@admin.register(AlertImageMultipleFolderPrivate)
class AlertImageMultipleFolderPrivateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'folder_code', 'is_checked', 'is_deleted', 'image_quantity', 'created_at', 'modified_at')
