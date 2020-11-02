# Generated by Django 3.1.2 on 2020-11-02 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_plotinfo_actualdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotinfo',
            name='actualdate',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 2, 15, 29, 8, 992648), editable=False),
        ),
        migrations.AlterField(
            model_name='plotinfo',
            name='fun',
            field=models.CharField(help_text='Введите вашу функцию от t', max_length=50),
        ),
        migrations.AlterField(
            model_name='plotinfo',
            name='interval',
            field=models.PositiveIntegerField(help_text='Интервал времени в днях'),
        ),
        migrations.AlterField(
            model_name='plotinfo',
            name='step',
            field=models.PositiveIntegerField(help_text='Шаг моделирования в часах'),
        ),
    ]