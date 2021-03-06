# Generated by Django 3.2.9 on 2022-01-16 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post_category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='post',
            name='post_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='blog.post_category'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_slug',
            field=models.CharField(default='default_post', max_length=80),
        ),
    ]
