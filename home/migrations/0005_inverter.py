# Generated by Django 2.2.7 on 2019-12-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20191215_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inverter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('input_voltage', models.IntegerField(help_text='Input voltage')),
                ('output_voltage', models.IntegerField(help_text='Output voltage')),
                ('watts', models.IntegerField(help_text='Watts')),
                ('price', models.DecimalField(decimal_places=2, help_text='Price in "dollars.cents"', max_digits=15)),
                ('kind', models.CharField(max_length=255)),
                ('image_url', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
