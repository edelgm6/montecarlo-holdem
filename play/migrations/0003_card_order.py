# Generated by Django 2.1.3 on 2018-11-24 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0002_auto_20181124_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
