# Generated by Django 3.1.2 on 2020-10-27 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_plotinfo_graph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotinfo',
            name='graph',
            field=models.TextField(editable=False),
        ),
    ]