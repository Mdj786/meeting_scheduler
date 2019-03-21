# Generated by Django 2.1.7 on 2019-03-12 10:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='task_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
