# Generated by Django 4.2.1 on 2023-06-21 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0004_camerasplitsetting_is_original_state_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='checked',
            new_name='is_checked',
        ),
        migrations.RenameField(
            model_name='alertprivate',
            old_name='checked',
            new_name='is_checked',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='name',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='alertprivate',
            name='name',
        ),
        migrations.RemoveField(
            model_name='alertprivate',
            name='quantity',
        ),
        migrations.AddField(
            model_name='alert',
            name='folder_code',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alert',
            name='folder_quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alert',
            name='image_code',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alert',
            name='image_quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alert',
            name='video_code',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alert',
            name='video_quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='folder_code',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='folder_quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='image_code',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='image_quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='video_code',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='alertprivate',
            name='video_quantity',
            field=models.IntegerField(default=1),
        ),
    ]
