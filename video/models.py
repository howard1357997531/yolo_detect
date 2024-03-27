from django.db import models
from django.contrib.auth.models import User
import os

USER_CHOICES = (
    ('guest', 'guest'),
    ('superuser', 'superuser'),
)

class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Video(models.Model):
    name = models.CharField(max_length=180)
    videofile = models.FileField(upload_to='video')  # 前面預設路徑 MEDIA_ROOT = BASE_DIR / 'static/media'

    def __str__(self):
        return self.name

def upload_to(request, filename):
    return os.path.join('video_private', request.user.username, filename)

class VideoPrivate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=180)
    videofile = models.FileField(upload_to=upload_to)

    def __str__(self):
        return str(self.user)

class VideoOutput(CommonInfo):
    user = models.CharField(max_length=180, choices=USER_CHOICES, default='guest')
    name = models.CharField(max_length=180, null=True, blank=True)
    file_url = models.CharField(max_length=180, null=True, blank=True)
    front_img_name_url = models.CharField(max_length=180, null=True, blank=True)

    def __str__(self):
        return self.name

class VideoOutputPrivate(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=180, null=True, blank=True)
    file_url = models.CharField(max_length=180, null=True, blank=True)
    front_img_name_url = models.CharField(max_length=180, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
class AlertVideo(CommonInfo):
    source = models.ForeignKey(VideoOutput, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.source.name
        super(AlertVideo, self).save(*args, **kwargs)

    def __str__(self):
        return self.source.name
    
class AlertVideoNormalUser(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(VideoOutputPrivate, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.source.name
        super(AlertVideoNormalUser, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
    
class AlertVideoSuperUser(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(VideoOutput, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.source.name
        super(AlertVideoSuperUser, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
