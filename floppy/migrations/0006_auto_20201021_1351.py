# Generated by Django 3.1.2 on 2020-10-21 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floppy', '0005_note_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
