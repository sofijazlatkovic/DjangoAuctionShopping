# Generated by Django 2.2.3 on 2019-09-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aukcije', '0003_prodaja_datum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodaja',
            name='krajnjacena',
            field=models.PositiveIntegerField(blank=True, db_column='krajnjaCena', verbose_name='Krajnja cena'),
        ),
    ]