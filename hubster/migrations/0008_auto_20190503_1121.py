# Generated by Django 2.2.1 on 2019-05-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubster', '0007_auto_20190503_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepo',
            name='node_id',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='githubuser',
            name='node_id',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='license',
            name='node_id',
            field=models.CharField(max_length=32),
        ),
    ]
