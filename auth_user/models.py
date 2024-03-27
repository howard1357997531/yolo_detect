from django.db import models
from django.contrib.auth.models import User

class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=180)
    email = models.EmailField(max_length=180)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    darkmode = models.BooleanField(default=False)
    album_date_sort = models.BooleanField(default=False)

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/undraw_profile.svg'
        return url

    def __str__(self):
        return str(self.user)
    
ITEM_CHOICES = (
    ('none', 'none'),
    ('image', 'image'),
    ('video', 'video'),
    ('folder', 'folder'),
    ('profile_setting', 'profile_setting'),
    ('password_change', 'password_change'),
    ('camera_setting', 'camera_setting'),
)
    
class Alert(CommonInfo):
    total_quantity = models.PositiveIntegerField(default=0)
    alert_image_code = models.PositiveIntegerField(default=0)
    alert_image_quantity = models.PositiveIntegerField(default=0)
    alert_video_code = models.PositiveIntegerField(default=0)
    alert_video_quantity = models.PositiveIntegerField(default=0)
    alert_folder_code = models.PositiveIntegerField(default=0)
    alert_folder_quantity = models.PositiveIntegerField(default=0)
    alert_pure_code = models.PositiveIntegerField(default=0)
    alert_pure_profile_setting_quantity = models.PositiveIntegerField(default=0)
    alert_pure_password_change_quantity = models.PositiveIntegerField(default=0)
    alert_pure_camera_setting_quantity = models.PositiveIntegerField(default=0)
    last_one_item = models.CharField(max_length=180, choices=ITEM_CHOICES, default='none')
    last_two_item = models.CharField(max_length=180, choices=ITEM_CHOICES, default='none')
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
class AlertPrivate(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total_quantity = models.PositiveIntegerField(default=0)
    alert_image_code = models.PositiveIntegerField(default=0)
    alert_image_quantity = models.PositiveIntegerField(default=0)
    alert_video_code = models.PositiveIntegerField(default=0)
    alert_video_quantity = models.PositiveIntegerField(default=0)
    alert_folder_code = models.PositiveIntegerField(default=0)
    alert_folder_quantity = models.PositiveIntegerField(default=0)
    alert_pure_code = models.PositiveIntegerField(default=0)
    alert_pure_profile_setting_quantity = models.PositiveIntegerField(default=0)
    alert_pure_password_change_quantity = models.PositiveIntegerField(default=0)
    alert_pure_camera_setting_quantity = models.PositiveIntegerField(default=0)
    last_one_item = models.CharField(max_length=180, choices=ITEM_CHOICES, default='none')
    last_two_item = models.CharField(max_length=180, choices=ITEM_CHOICES, default='none')
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

# 因為在mainapp裡，yolo也有預設一個models資料夾，這會跟django models資料夾衝突到(在import時)
# 兩個models都不能輕易地更改名稱，所以把mainapp裡需要的model寫在這裡
class CameraSplitSetting(CommonInfo):
    camera_name = models.CharField(max_length=180, null=True, blank=True)
    is_original_state = models.BooleanField(default=True)
    x_start = models.FloatField(default=0)
    x_end = models.FloatField(default=1)
    y_start = models.FloatField(default=0)
    y_end = models.FloatField(default=1)

    def __str__(self):
        return self.camera_name

class CameraSplitSettingPrivate(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_original_state = models.BooleanField(default=True)
    camera_name = models.CharField(max_length=180, null=True, blank=True)
    x_start = models.FloatField(default=0)
    x_end = models.FloatField(default=1)
    y_start = models.FloatField(default=0)
    y_end = models.FloatField(default=1)

    def __str__(self):
        return self.camera_name

# 單純紀錄數量的alert
AlertTypeChoices = (
    ('profile_setting', 'profile_setting'),
    ('password_change', 'password_change'),
    ('camera_setting', 'camera_setting'),
)

class AlertPureQuantity(CommonInfo):
    name = models.CharField(max_length=180, choices=AlertTypeChoices)
    code = models.PositiveBigIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class AlertPureQuantityPrivate(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=180, choices=AlertTypeChoices)
    code = models.PositiveBigIntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)
