# Generated by Django 4.0.3 on 2023-05-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_task_parent_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_started',
            field=models.BooleanField(default=False),
        ),
    ]
