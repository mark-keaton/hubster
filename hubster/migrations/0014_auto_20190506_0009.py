# Generated by Django 2.2.1 on 2019-05-06 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubster', '0013_auto_20190506_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepo',
            name='homepage',
            field=models.URLField(null=True),
        ),
    ]