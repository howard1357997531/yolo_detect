# Generated by Django 4.2.1 on 2023-05-22 08:48

from django.db import migrations, models
import image.models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageMultipleFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(default=1)),
                ('name', models.CharField(max_length=180)),
                ('image_file', models.ImageField(upload_to=image.models.upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='imageprivate',
            name='image_file',
            field=models.ImageField(upload_to=image.models.upload_to),
        ),
    ]
