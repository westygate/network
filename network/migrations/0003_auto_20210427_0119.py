# Generated by Django 3.1.7 on 2021-04-26 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210425_2149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['timestamp']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes_count',
        ),
    ]
