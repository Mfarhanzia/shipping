# Generated by Django 2.2.3 on 2019-08-23 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190818_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Username'),
        ),
    ]
