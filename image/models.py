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

class Image(CommonInfo):
    user = models.CharField(max_length=180, choices=USER_CHOICES, default='guest')
    name = models.CharField(max_length=180)
    image_file = models.ImageField(upload_to='image')

    def __str__(self):
        return self.name

def upload_to(request, filename):
    return os.path.join('image', request.user.username, filename)

class ImagePrivate(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=180)
    image_file = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return str(self.user)
    
def upload_to(instance, filename):
    return os.path.join('image_multiple_folder', str(instance.code), filename)
    
class ImageMultipleFolder(CommonInfo):
    user = models.CharField(max_length=180, choices=USER_CHOICES, default='guest')
    code = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=180)
    image_file = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return self.name
    
def upload_to(instance, filename):
    return os.path.join('image_multiple_folder_private', instance.user.username, str(instance.code), filename)
    
class ImageMultipleFolderPrivate(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=180)
    image_file = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return self.name
    
class AlertImage(CommonInfo):
    source = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.source.name
        super(AlertImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.source.name
    
class AlertImageNormalUser(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(ImagePrivate, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.source.name
        super(AlertImageNormalUser, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
    
class AlertImageSuperUser(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.source.name
        super(AlertImageSuperUser, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
    
class AlertImageMultipleFolder(CommonInfo):
    code = models.PositiveIntegerField(default=1)
    folder_code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    image_quantity = models.PositiveIntegerField(default=0)
    delete_quantity = models.PositiveIntegerField(default=0)
    total_quantity = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_quantity = self.image_quantity - self.delete_quantity
        super(AlertImageMultipleFolder, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.code)
    
class AlertImageMultipleFolderPrivate(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.PositiveIntegerField(default=1)
    folder_code = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    image_quantity = models.PositiveIntegerField(default=0)
    delete_quantity = models.PositiveIntegerField(default=0)
    total_quantity = models.PositiveIntegerField(default=0)

    # 只要有再views使用.save()都會觸發
    def save(self, *args, **kwargs):
        self.total_quantity = self.image_quantity - self.delete_quantity
        super(AlertImageMultipleFolderPrivate, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
