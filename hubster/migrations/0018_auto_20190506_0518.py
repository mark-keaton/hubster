# Generated by Django 2.2.1 on 2019-05-06 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubster', '0017_auto_20190506_0514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]