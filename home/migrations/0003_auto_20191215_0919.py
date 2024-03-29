# Generated by Django 2.2.7 on 2019-12-15 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20191210_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='solarpanel',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='solarpanel',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price of the panel in "dollars.cents"', max_digits=15),
        ),
        migrations.AlterField(
            model_name='solarpanel',
            name='weight',
            field=models.IntegerField(help_text='Weight of the panel in grams'),
        ),
    ]
