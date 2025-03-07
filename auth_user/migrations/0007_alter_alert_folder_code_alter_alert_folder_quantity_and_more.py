# Generated by Django 4.2.1 on 2023-06-21 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0006_alter_alert_folder_code_alter_alert_folder_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='folder_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='folder_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='image_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='video_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='video_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='folder_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='folder_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='image_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='image_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='video_code',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertprivate',
            name='video_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
