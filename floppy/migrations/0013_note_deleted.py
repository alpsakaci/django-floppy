# Generated by Django 3.1.2 on 2020-11-11 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floppy', '0012_auto_20201105_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]