# Generated by Django 2.2.1 on 2019-05-03 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubster', '0005_auto_20190503_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepo',
            name='license',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hubster.License'),
        ),
    ]
