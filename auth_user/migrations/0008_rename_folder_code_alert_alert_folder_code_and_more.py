# Generated by Django 4.2.1 on 2023-06-21 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0007_alter_alert_folder_code_alter_alert_folder_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='folder_code',
            new_name='alert_folder_code',
        ),
        migrations.RenameField(
            model_name='alert',
            old_name='folder_quantity',
            new_name='alert_folder_quantity',
        ),
        migrations.RenameField(
            model_name='alert',
            old_name='image_code',
            new_name='alert_image_code',
        ),
        migrations.RenameField(
            model_name='alert',
            old_name='image_quantity',
            new_name='alert_image_quantity',
        ),
        migrations.RenameField(
            model_name='alert',
            old_name='video_code',
            new_name='alert_video_code',
        ),
        migrations.RenameField(
            model_name='alert',
            old_name='video_quantity',
            new_name='alert_video_quantity',
        ),
        migrations.RenameField(
            model_name='alertprivate',
            old_name='folder_code',
            new_name='alert_folder_code',
        ),
        migrations.RenameField(
            model_name='alertprivate',
            old_name='folder_quantity',
            new_name='alert_folder_quantity',
        ),
        migrations.RenameField(
            model_name='alertprivate',
            old_name='image_code',
            new_name='alert_image_code',
        ),
        migrations.RenameField(
            model_name='alertprivate',
            old_name='image_quantity',
            new_name='alert_image_quantity',
        ),
        migrations.RenameField(
            model_name='alertprivate',
            old_name='video_code',
            new_name='alert_video_code',
        ),
        migrations.RenameField(
            model_name='alertprivate',
            old_name='video_quantity',
            new_name='alert_video_quantity',
        ),
    ]