# Generated by Django 2.2.7 on 2019-12-15 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_inverter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battery',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price of the component in "dollars.cents"', max_digits=15),
        ),
        migrations.AlterField(
            model_name='inverter',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price of the component in "dollars.cents"', max_digits=15),
        ),
        migrations.AlterField(
            model_name='solarpanel',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price of the component in "dollars.cents"', max_digits=15),
        ),
    ]