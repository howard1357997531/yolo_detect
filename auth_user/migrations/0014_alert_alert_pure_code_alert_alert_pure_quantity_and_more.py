# Generated by Django 4.2.1 on 2023-07-03 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0013_alertpurequantity_is_checked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='alert_pure_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='alert',
            name='alert_pure_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='alert_pure_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='alert_pure_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='last_one_item',
            field=models.CharField(choices=[('none', 'none'), ('image', 'image'), ('video', 'video'), ('folder', 'folder'), ('profile_setting', 'profile_setting'), ('password_change', 'password_change'), ('camera_setting', 'camera_setting')], default='none', max_length=180),
        ),
        migrations.AlterField(
            model_name='alert',
            name='last_two_item',
            field=models.CharField(choices=[('none', 'none'), ('image', 'image'), ('video', 'video'), ('folder', 'folder'), ('profile_setting', 'profile_setting'), ('password_change', 'password_change'), ('camera_setting', 'camera_setting')], default='none', max_length=180),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='last_one_item',
            field=models.CharField(choices=[('none', 'none'), ('image', 'image'), ('video', 'video'), ('folder', 'folder'), ('profile_setting', 'profile_setting'), ('password_change', 'password_change'), ('camera_setting', 'camera_setting')], default='none', max_length=180),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='last_two_item',
            field=models.CharField(choices=[('none', 'none'), ('image', 'image'), ('video', 'video'), ('folder', 'folder'), ('profile_setting', 'profile_setting'), ('password_change', 'password_change'), ('camera_setting', 'camera_setting')], default='none', max_length=180),
        ),
    ]
