# Generated by Django 4.2.1 on 2023-05-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_room_children_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='rooms',
            field=models.ManyToManyField(related_name='hotels', to='api.room'),
        ),
    ]
