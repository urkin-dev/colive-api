# Generated by Django 4.2.1 on 2023-06-04 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_place_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='meal',
            field=models.BooleanField(default=True),
        ),
    ]
