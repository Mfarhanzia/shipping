# Generated by Django 2.2.3 on 2019-07-28 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20190726_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.AlterField(
            model_name='order',
            name='how_much_letter_of_credit',
            field=models.CharField(blank=True, help_text='in USD$', max_length=50, null=True, verbose_name='What is the value of your Letter of Credit (in USD)?'),
        ),
        migrations.AlterField(
            model_name='order',
            name='how_much_line_of_credit',
            field=models.CharField(blank=True, help_text='in USD$', max_length=50, null=True, verbose_name='What is the currently unused amount in your Line of Credit?'),
        ),
    ]
