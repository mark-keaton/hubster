# Generated by Django 2.2.1 on 2019-05-05 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubster', '0009_auto_20190505_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubuser',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
