# Generated by Django 3.1.4 on 2021-01-23 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='tweet_text',
            field=models.CharField(max_length=360),
        ),
    ]
