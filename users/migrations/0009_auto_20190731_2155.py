# Generated by Django 2.2.3 on 2019-07-31 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190730_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name of Company'),
        ),
        migrations.AlterField(
            model_name='specialuser',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Title'),
        ),
    ]
