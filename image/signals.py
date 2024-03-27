from django.db.models.signals import post_save ,pre_delete
from django.dispatch import receiver
from django.conf import settings
from .models import (Image, ImagePrivate, ImageMultipleFolder, ImageMultipleFolderPrivate,
                     AlertImage, AlertImageNormalUser, AlertImageSuperUser,
                     AlertImageMultipleFolder, AlertImageMultipleFolderPrivate)
from auth_user.models import Alert, AlertPrivate
import os

@receiver(pre_delete, sender=Image)
def ImageSignals(sender, instance, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'image', instance.name))
    except:
        pass

@receiver(pre_delete, sender=ImagePrivate)
def ImagePrivateSignals(sender, instance, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'image', instance.user.username, instance.name))
    except:
        pass

@receiver(pre_delete, sender=ImageMultipleFolder)
def ImageMultipleFolderDeleteSignals(sender, instance, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'image_multiple_folder', str(instance.code), instance.name))
        if not os.listdir(os.path.join(settings.MEDIA_ROOT, 'image_multiple_folder', str(instance.code))):
            os.rmdir(os.path.join(settings.MEDIA_ROOT, 'image_multiple_folder', str(instance.code)))     
    except:
        pass

@receiver(pre_delete, sender=ImageMultipleFolderPrivate)
def ImageMultipleFolderDeletePrivateSignals(sender, instance, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'image_multiple_folder_private', instance.user.username, str(instance.code), instance.name))
        if not os.listdir(os.path.join(settings.MEDIA_ROOT, 'image_multiple_folder_private', instance.user.username, str(instance.code))):
            os.rmdir(os.path.join(settings.MEDIA_ROOT, 'image_multiple_folder_private', instance.user.username, str(instance.code)))    
    except:
        pass

# alert
@receiver(post_save, sender=AlertImage)
def AlertImageSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = Alert.objects.get_or_create(is_checked=False)
        alert.total_quantity += 1
        alert.alert_image_code = instance.code
        alert.alert_image_quantity += 1

        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'image'
        else:
            if last_one_item != 'image':
                alert.last_one_item = 'image'
                alert.last_two_item = last_one_item
        '''
        如果使用下述部分更新，不會更新 modified_at 
        alert.save(update_fields=['total_quantity', 'alert_image_code', 'alert_image_quantity'])
        '''
        alert.save()

@receiver(post_save, sender=AlertImageNormalUser)
def AlertImageNormalUserSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = AlertPrivate.objects.get_or_create(user=instance.user, is_checked=False)
        alert.total_quantity += 1
        alert.alert_image_code = instance.code
        alert.alert_image_quantity += 1

        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'image'
        else:
            if last_one_item != 'image':
                alert.last_one_item = 'image'
                alert.last_two_item = last_one_item
        alert.save()

@receiver(post_save, sender=AlertImageSuperUser)
def AlertImageSuperUserSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = AlertPrivate.objects.get_or_create(user=instance.user, is_checked=False)
        alert.total_quantity += 1
        alert.alert_image_code = instance.code
        alert.alert_image_quantity += 1

        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'image'
        else:
            if last_one_item != 'image':
                alert.last_one_item = 'image'
                alert.last_two_item = last_one_item
        alert.save()

@receiver(post_save, sender=AlertImageMultipleFolder)
def AlertImageMultipleFolderSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = Alert.objects.get_or_create(is_checked=False)
        alert.total_quantity += 1
        alert.alert_folder_code = instance.code
        alert.alert_folder_quantity += 1

        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'folder'
        else:
            if last_one_item != 'folder':
                alert.last_one_item = 'folder'
                alert.last_two_item = last_one_item
        alert.save()

@receiver(post_save, sender=AlertImageMultipleFolderPrivate)
def AlertImageMultipleFolderPrivateSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = AlertPrivate.objects.get_or_create(user=instance.user, is_checked=False)
        alert.total_quantity += 1
        alert.alert_folder_code = instance.code
        alert.alert_folder_quantity += 1

        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'folder'
        else:
            if last_one_item != 'folder':
                alert.last_one_item = 'folder'
                alert.last_two_item = last_one_item
        alert.save()