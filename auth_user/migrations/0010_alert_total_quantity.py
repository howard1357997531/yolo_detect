# Generated by Django 4.2.1 on 2023-06-26 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0009_alertprivate_total_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='total_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
