from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Alert, AlertPrivate, AlertPureQuantity, AlertPureQuantityPrivate
from image.models import (AlertImage, AlertImageNormalUser, AlertImageSuperUser,
                          AlertImageMultipleFolder, AlertImageMultipleFolderPrivate)
from video.models import AlertVideo, AlertVideoNormalUser, AlertVideoSuperUser

# 登入也會觸發(不一定是創建)
@receiver(pre_save, sender=User)
def EmailCheckSignal(sender, instance, **kwargs):
    email = instance.email
    a = sender.objects.all()
    print(instance.username)
    for i in a:
        print(i.username)
    if sender.objects.filter(email=email).exclude(username=instance.username).exists():
        print('email exist')
        # raise ValidationError('Email Already Exists')

@receiver(post_save, sender=User)
def ProfileSignal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,
                               name=instance.first_name,
                               email = instance.email)
        
@receiver(post_save, sender=Profile)
def ProfileEmailSignal(sender, instance, created, **kwargs):
    if not created:
        user = User.objects.get(id=instance.user.id)
        user.email = instance.email
        user.save()

@receiver(pre_delete, sender=AlertPrivate)
def AlertPrivateSignal(sender, instance, **kwargs):
    if instance.alert_image_code > 0:
        if AlertImageSuperUser.objects.filter(user=instance.user).exists():
            images = AlertImageSuperUser.objects.filter(user=instance.user, code=instance.alert_image_code)
        else:
            images = AlertImageNormalUser.objects.filter(user=instance.user, code=instance.alert_image_code)
        for image in images:
            image.delete()
    
    if instance.alert_video_code > 0:
        if AlertVideoSuperUser.objects.filter(user=instance.user).exists():
            videos = AlertVideoSuperUser.objects.filter(user=instance.user, code=instance.alert_video_code)
        else:
            videos = AlertVideoNormalUser.objects.filter(user=instance.user, code=instance.alert_video_code)
        for video in videos:
            video.delete()
    
    if instance.alert_folder_code > 0:
        if AlertImageMultipleFolderPrivate.objects.filter(user=instance.user).exists():
            folder = AlertImageMultipleFolderPrivate.objects.filter(user=instance.user, code=instance.alert_folder_code).first()
            folder.delete()

    if instance.alert_pure_code > 0:
        if AlertPureQuantityPrivate.objects.filter(user=instance.user).exists():
            pures = AlertPureQuantityPrivate.objects.filter(user=instance.user, code=instance.alert_pure_code)
            for pure in pures:
                pure.delete()

@receiver(pre_delete, sender=Alert)
def AlertSignal(sender, instance, **kwargs):
    if instance.alert_image_code > 0:
        if AlertImage.objects.exists():
            images = AlertImage.objects.filter(code=instance.alert_image_code)
            for image in images:
                image.delete()
    
    if instance.alert_video_code > 0:
        if AlertVideo.objects.exists():
            videos = AlertVideo.objects.filter(code=instance.alert_video_code)
            for video in videos:
                video.delete()
    
    if instance.alert_folder_code > 0:
        if AlertImageMultipleFolder.objects.exists():
            folder = AlertImageMultipleFolder.objects.filter(code=instance.alert_folder_code).first()
            folder.delete()

    if instance.alert_pure_code > 0:
        if AlertPureQuantity.objects.exists():
            pures = AlertPureQuantity.objects.filter(code=instance.alert_pure_code)
            for pure in pures:
                pure.delete()
