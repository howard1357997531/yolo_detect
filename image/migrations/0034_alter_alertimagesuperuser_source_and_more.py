# Generated by Django 4.2.1 on 2023-06-27 08:03

from django.db import migrations, models
import django.db.models.deletion
import image.models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0033_alter_imagemultiplefolder_image_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertimagesuperuser',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='image.image'),
        ),
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
