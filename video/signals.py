from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from .models import VideoOutput, VideoOutputPrivate, AlertVideo, AlertVideoNormalUser, AlertVideoSuperUser
from auth_user.models import Alert, AlertPrivate
import os

@receiver(pre_delete, sender=VideoOutput)
def VideoOutputSignals(sender, instance, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'video_output', instance.name))
        os.remove(os.path.join(settings.MEDIA_ROOT, 'video_front_img', instance.name.replace('.mp4', '.png')))
    except:
        pass

@receiver(pre_delete, sender=VideoOutputPrivate)
def VideoOutputPrivateSignals(sender, instance, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'video_output', instance.user.username, instance.name))
        os.remove(os.path.join(settings.MEDIA_ROOT, 'video_front_img', instance.user.username, instance.name.replace('.mp4', '.png')))
    except:
        pass

@receiver(post_save, sender=AlertVideo)
def AlertVideoSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = Alert.objects.get_or_create(is_checked=False)
        alert.total_quantity += 1
        alert.alert_video_code = instance.code
        alert.alert_video_quantity += 1
        
        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'video'
        else:
            if last_one_item != 'video':
                alert.last_one_item = 'video'
                alert.last_two_item = last_one_item
        alert.save()

@receiver(post_save, sender=AlertVideoNormalUser)
def AlertVideoNormalUserSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = AlertPrivate.objects.get_or_create(user=instance.user, is_checked=False)
        alert.total_quantity += 1
        alert.alert_video_code = instance.code
        alert.alert_video_quantity += 1
        
        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'video'
        else:
            if last_one_item != 'video':
                alert.last_one_item = 'video'
                alert.last_two_item = last_one_item
        alert.save()

@receiver(post_save, sender=AlertVideoSuperUser)
def AlertVideoSuperUserSignals(sender, instance, created, **kwargs):
    if created:
        alert, inner_created = AlertPrivate.objects.get_or_create(user=instance.user, is_checked=False)
        alert.total_quantity += 1
        alert.alert_video_code = instance.code
        alert.alert_video_quantity += 1
        
        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'video'
        else:
            if last_one_item != 'video':
                alert.last_one_item = 'video'
                alert.last_two_item = last_one_item
        alert.save()
