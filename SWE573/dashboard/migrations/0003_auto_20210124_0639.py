# Generated by Django 3.1.4 on 2021-01-24 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20210123_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='tweet_text',
            field=models.CharField(max_length=500),
        ),
    ]