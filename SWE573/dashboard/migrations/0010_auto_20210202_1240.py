# Generated by Django 3.1.4 on 2021-02-02 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20210130_1100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweets',
            name='isSaved',
        ),
        migrations.RemoveField(
            model_name='tweets',
            name='saved_search_alias',
        ),
    ]