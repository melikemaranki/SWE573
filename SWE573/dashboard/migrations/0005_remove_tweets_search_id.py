# Generated by Django 3.1.4 on 2021-01-11 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20210111_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweets',
            name='search_id',
        ),
    ]