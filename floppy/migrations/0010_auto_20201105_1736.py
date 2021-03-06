# Generated by Django 3.1.2 on 2020-11-05 14:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('floppy', '0009_notelog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notelog',
            name='date_log',
        ),
        migrations.AddField(
            model_name='notelog',
            name='action_flag',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Addition'), (2, 'Change'), (3, 'Deletion')], default=1, verbose_name='action flag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notelog',
            name='action_time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='action time'),
        ),
    ]
