# Generated by Django 4.2.1 on 2023-06-28 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_alter_alertvideo_source_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertvideosuperuser',
            name='name',
            field=models.CharField(blank=True, max_length=180, null=True),
        ),
    ]