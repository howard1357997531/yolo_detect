# Generated by Django 4.2.1 on 2023-06-20 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('image', '0015_imagemultiplefolderalert_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImageAlertPrivate',
            new_name='ImageAlertNormalUser',
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
        migrations.CreateModel(
            name='ImageAlertSuperUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('code', models.PositiveIntegerField(default=1)),
                ('is_checked', models.BooleanField(default=False)),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='image.image')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
