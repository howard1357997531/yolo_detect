# Generated by Django 4.2.1 on 2023-06-05 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videooutput',
            name='front_img_name_url',
            field=models.CharField(blank=True, max_length=180, null=True),
        ),
        migrations.AddField(
            model_name='videooutputprivate',
            name='front_img_name_url',
            field=models.CharField(blank=True, max_length=180, null=True),
        ),
        migrations.AlterField(
            model_name='videooutput',
            name='file_url',
            field=models.CharField(blank=True, max_length=180, null=True),
        ),
        migrations.AlterField(
            model_name='videooutput',
            name='name',
            field=models.CharField(blank=True, max_length=180, null=True),
        ),
        migrations.AlterField(
            model_name='videooutputprivate',
            name='file_url',
            field=models.CharField(blank=True, max_length=180, null=True),
        ),
        migrations.AlterField(
            model_name='videooutputprivate',
            name='name',
            field=models.CharField(blank=True, max_length=180, null=True),
        ),
    ]
