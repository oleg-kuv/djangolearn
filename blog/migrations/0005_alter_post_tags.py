# Generated by Django 3.2.19 on 2023-08-05 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_tag_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='Теги'),
        ),
    ]