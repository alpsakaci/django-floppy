# Generated by Django 3.1.2 on 2020-11-11 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('floppy', '0014_notecaretaker_notememento'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NoteLog',
        ),
    ]