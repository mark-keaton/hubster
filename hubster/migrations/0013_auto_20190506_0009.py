# Generated by Django 2.2.1 on 2019-05-06 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubster', '0012_auto_20190506_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepo',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
