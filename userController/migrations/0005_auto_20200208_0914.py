# Generated by Django 3.0 on 2020-02-08 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userController', '0004_auto_20200207_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='spoken_languages',
            field=models.TextField(default='en', max_length=100),
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]
