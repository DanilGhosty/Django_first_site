# Generated by Django 3.2.9 on 2022-05-16 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_message_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_created',
            field=models.TimeField(auto_now=True),
        ),
    ]
