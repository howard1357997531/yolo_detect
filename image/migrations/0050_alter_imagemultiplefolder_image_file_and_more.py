# Generated by Django 4.2.1 on 2023-07-04 08:54

from django.db import migrations, models
import image.models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0049_alter_imagemultiplefolder_image_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemultiplefolder',
            name='image_file',
            field=models.ImageField(upload_to=image.models.upload_to),
        ),
        migrations.AlterField(
            model_name='imageprivate',
            name='image_file',
            field=models.ImageField(upload_to=image.models.upload_to),
        ),
    ]
