# Generated by Django 2.2.3 on 2019-09-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aukcije', '0007_auto_20190904_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocena',
            name='ocenio',
            field=models.CharField(max_length=10),
        ),
    ]