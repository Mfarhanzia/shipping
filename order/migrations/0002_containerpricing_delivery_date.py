# Generated by Django 2.1 on 2019-12-12 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='containerpricing',
            name='delivery_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
