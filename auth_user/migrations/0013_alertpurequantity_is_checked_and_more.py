# Generated by Django 4.2.1 on 2023-07-03 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0012_alertpurequantity_alertpurequantityprivate'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertpurequantity',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alertpurequantityprivate',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
    ]
