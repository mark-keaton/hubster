# Generated by Django 2.2.1 on 2019-05-06 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubster', '0015_auto_20190506_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepo',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='githubrepo',
            name='pushed_at',
            field=models.DateTimeField(null=True),
        ),
    ]