# Generated by Django 2.1.3 on 2018-11-24 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0005_auto_20181124_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='stack',
            new_name='hand',
        ),
    ]
