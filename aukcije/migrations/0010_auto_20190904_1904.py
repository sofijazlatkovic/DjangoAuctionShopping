# Generated by Django 2.2.3 on 2019-09-04 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aukcije', '0009_auto_20190904_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocena',
            name='ocena',
            field=models.CharField(max_length=10),
        ),
    ]