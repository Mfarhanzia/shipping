# Generated by Django 2.1 on 2019-12-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20191222_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='user_image',
            field=models.ImageField(blank=True, default='default.jpeg', null=True, upload_to='pdf-image'),
        ),
    ]
