# Generated by Django 3.0 on 2020-02-11 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userController', '0008_auto_20200211_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.CharField(blank=True, max_length=500, verbose_name='URL to your Profile Picture'),
        ),
    ]
